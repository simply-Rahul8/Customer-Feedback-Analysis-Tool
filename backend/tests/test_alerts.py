from backend.main import submit_feedback
from backend.fallback import rule_based_analysis
from backend.llm_client import analyze_feedback
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

#def test_provider_failure_uses_fallback(mocker):
    # Force LLM to raise an error
#    mocker.patch("backend.llm_client.analyze_feedback", side_effect=Exception("LLM Down"))

#    payload = {"text": "The app is too slow!"}

#    response = client.post("/feedback", json=payload)
#    data = response.json()

    # Should still return 200 OK
#    assert response.status_code == 200

    # Should use fallback rules
#    assert data["sentiment"] in ["Negative", "neutral", "positive"]
#    assert "slow" in data["topics"].lower()
