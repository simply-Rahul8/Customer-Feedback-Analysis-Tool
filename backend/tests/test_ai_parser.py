from backend.llm_client import parse_llm_output

def test_parse_llm_output_basic():
    raw = """
    Sentiment: Positive
    Topics: app update, login speed
    Alert: Yes
    """

    sentiment, topics, alert = parse_llm_output(raw)

    assert sentiment == "Positive"
    assert topics == "app update, login speed"
    assert alert == "Yes"
