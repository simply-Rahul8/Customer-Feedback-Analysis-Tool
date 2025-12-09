from backend.fallback import rule_based_analysis

def test_fallback_alert_triggers():
    text = "The app crashes and I cannot login!"
    result = rule_based_analysis(text)

    assert result["alert"] == "Yes"
    assert "crash" in result["topics"].lower()
