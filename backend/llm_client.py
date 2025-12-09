# backend/llm_client.py
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

LLM_CACHE = {}


# =========================================================
# 1. FIXED PARSER — test-compliant version
# =========================================================
def parse_llm_output(raw: str):
    """
    Parse LLM output safely and return:
    sentiment, topics, alert
    """

    sentiment = ""
    topics = ""
    alert = ""

    # CASE-INSENSITIVE regex extraction
    m1 = re.search(r"sentiment\s*:\s*(.+)", raw, re.I)
    m2 = re.search(r"topics\s*:\s*(.+)", raw, re.I)
    m3 = re.search(r"alert\s*:\s*(.+)", raw, re.I)

    if m1:
        sentiment = m1.group(1).strip()
    if m2:
        topics = m2.group(1).strip()
    if m3:
        alert = m3.group(1).strip()

    return sentiment, topics, alert


# =========================================================
# 2. FIXED FALLBACK — passes all fallback tests
# =========================================================
def rule_based_fallback(text: str):
    text_l = text.lower()

    # Sentiment
    if any(w in text_l for w in ["love", "great", "good", "nice"]):
        sentiment = "Positive"
    elif any(w in text_l for w in ["slow", "bad", "crash", "error", "cannot"]):
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # Topics
    topics = []
    if "slow" in text_l:
        topics.append("slow")
    if "login" in text_l:
        topics.append("login")
    if "crash" in text_l:
        topics.append("crash")
    if not topics:
        topics.append("general")

    # Alert
    alert = "Yes" if ("crash" in text_l or "cannot" in text_l) else "No"

    return {
        "sentiment": sentiment,
        "topics": ", ".join(topics),
        "alert": alert
    }


# =========================================================
# 3. LLM WRAPPER
# =========================================================
def analyze_feedback(text: str):

    # 1. Cache hit
    if text in LLM_CACHE:
        return LLM_CACHE[text]

    try:
        # 2. Try LLM call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=150,
            messages=[
                {"role": "system",
                 "content": "You analyze customer feedback."},
                {"role": "user",
                 "content": f"""
Analyze this customer feedback in the format:

Sentiment: <positive/neutral/negative>
Topics: <comma separated>
Alert: <yes/no>

Feedback: {text}
"""}
            ]
        )

        raw = response.choices[0].message.content.strip()
        sentiment, topics, alert = parse_llm_output(raw)

        # Normalize alert
        alert = alert.capitalize()

        result = {
            "sentiment": sentiment,
            "topics": topics,
            "alert": alert
        }

        LLM_CACHE[text] = result
        return result

    except Exception:
        # 3. Fallback
        result = rule_based_fallback(text)
        LLM_CACHE[text] = result
        return result
