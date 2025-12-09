from fastapi.testclient import TestClient
from backend.main import app
from backend.cache import get_cached_result
from backend.models import Feedback

client = TestClient(app)

def test_full_pipeline_integration():
    text = "Login page is very slow"

    response = client.post("/feedback", json={"text": text})
    assert response.status_code == 200

    data = response.json()
    assert data["text"] == text
    assert data["sentiment"] is not None
    assert data["topics"] is not None
    assert data["alert"] in ["Yes", "No"]

    # Fetch recent feedback
    recent = client.get("/feedback/recent")
    assert recent.status_code == 200

    records = recent.json()
    assert len(records) >= 1
