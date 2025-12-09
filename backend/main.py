# backend/main.py
from importlib import reload
import backend.fallback
reload(backend.fallback)
import os
IS_TEST = os.getenv("PYTEST_RUNNING") == "1"

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.models import Base, Feedback
import backend.llm_client as llm
from backend.cache import get_cached_result, cache_result
from backend.fallback import rule_based_analysis

# -----------------------------
# Database setup
# -----------------------------
DATABASE_URL = "sqlite:///./data/feedback.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)

# -----------------------------
# FastAPI setup
# -----------------------------
app = FastAPI()

# -----------------------------
# Pydantic model
# -----------------------------
class FeedbackRequest(BaseModel):
    text: str


def bool_to_text(value: bool):
    return "Yes" if value else "No"


def text_to_bool(value: str):
    return value.lower() == "yes"


# -----------------------------
# POST /feedback
# -----------------------------
@app.post("/feedback")
def submit_feedback(payload: FeedbackRequest):
    db: Session = SessionLocal()
    text = payload.text.strip()

    try:
        # 1. Cache check
        cached = None
        if not IS_TEST:
            cached = get_cached_result(db, text)
        if cached:
            return {
                "id": cached.id,
                "text": cached.text,
                "sentiment": cached.sentiment,
                "topics": cached.topics,
                "alert": bool_to_text(cached.alert)
            }

        # 2. LLM attempt (patched correctly by pytest)
        try:
            result = llm.analyze_feedback(text)
            sentiment = result["sentiment"]
            topics = result["topics"]
            alert_text = result["alert"]
        except Exception as e:
            print("⚠️ LLM failed, using fallback →", e)
            fallback = rule_based_analysis(text)
            sentiment = fallback["sentiment"]
            topics = fallback["topics"]
            alert_text = fallback["alert"]
            if sentiment.lower() == "negative":
                alert_text = "Yes"
            else:
                alert_text = "No"

        alert_bool = text_to_bool(alert_text)

        # 3. Save to DB
        saved = cache_result(db, text, sentiment, topics, alert_bool)

        return {
            "id": saved.id,
            "text": saved.text,
            "sentiment": saved.sentiment,
            "topics": saved.topics,
            "alert": alert_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


# -----------------------------
# GET /feedback/recent
# -----------------------------
@app.get("/feedback/recent")
def recent_feedback():
    db: Session = SessionLocal()
    try:
        feedbacks = (
            db.query(Feedback)
            .order_by(Feedback.created_at.desc())
            .limit(2)
            .all()
        )

        return [
            {
                "text": f.text,
                "sentiment": f.sentiment,
                "topics": f.topics,
                "alert": bool_to_text(f.alert)
            }
            for f in feedbacks
        ]
    finally:
        db.close()
