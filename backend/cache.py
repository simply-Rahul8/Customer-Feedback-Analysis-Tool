# backend/cache.py
from sqlalchemy.orm import Session
from backend.models import Feedback

def get_cached_result(db: Session, text: str):
    """Return cached feedback analysis if already processed."""
    return (
        db.query(Feedback)
          .filter(Feedback.text == text)
          .order_by(Feedback.id.desc())
          .first()
    )

def cache_result(db, text, sentiment, topics, alert):

    # Normalize alert to Yes/No
    if alert in (0, 1, True, False):
        alert = "Yes" if alert in (1, True) else "No"

    entry = Feedback(
        text=text,
        sentiment=sentiment,
        topics=topics,
        alert=alert
    )

    db.add(entry)
    db.commit()       # ← REQUIRED
    db.refresh(entry) # ← REQUIRED

    return entry