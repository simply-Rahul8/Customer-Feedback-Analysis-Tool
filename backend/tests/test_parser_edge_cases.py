from backend.llm_client import parse_llm_output

def test_parser_missing_lines():
    raw = "Sentiment: Positive"
    sentiment, topics, alert = parse_llm_output(raw)

    assert sentiment == "Positive"
    assert topics == ""
    assert alert == ""


def test_parser_garbage_input():
    raw = "?????????"
    sentiment, topics, alert = parse_llm_output(raw)

    assert sentiment == ""
    assert topics == ""
    assert alert == ""
