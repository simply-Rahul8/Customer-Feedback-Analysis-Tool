# backend/tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, Feedback

@pytest.fixture
def test_db():
    # Use in-memory SQLite (fastest)
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine)

    # Create tables
    Base.metadata.create_all(engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
def mock_openai(mocker):
    mocker.patch(
        "backend.llm_client.analyze_feedback",
        return_value="""
            Sentiment: Neutral
            Topics: login speed, ux
            Alert: No
        """
    )