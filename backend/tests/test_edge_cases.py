#from fastapi.testclient import TestClient
#from backend.main import app

#client = TestClient(app)

#def test_empty_feedback():
#    response = client.post("/feedback", json={"text": ""})
#    data = response.json()
#    assert response.status_code == 200
#    assert data["sentiment"] is not None  # fallback still handles it


#def test_emoji_only_feedback():
#    response = client.post("/feedback", json={"text": "😡🔥"})
#    data = response.json()

#    assert response.status_code == 200
#    assert data["sentiment"] in ["Positive", "Negative", "Neutral"]
#    assert isinstance(data["topics"], str)
#    assert data["alert"] in ["Yes", "No"]


#def test_swedish_feedback():
#    response = client.post("/feedback", json={"text": "Appen är långsam och kraschar ibland"})
#    data = response.json()

#    assert response.status_code == 200
#    assert "slow" in data["topics"].lower() or "crash" in data["topics"].lower()


#def test_huge_feedback():
#    long_text = "good " * 2000  # 10k chars
#    response = client.post("/feedback", json={"text": long_text})
#    assert response.status_code == 200
#