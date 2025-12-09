# backend/fallback.py

def rule_based_analysis(text: str):
    t = text.lower()
    topics = []

    # ---------- TOPIC DETECTION ----------
    # SPEED / PERFORMANCE
    if any(word in t for word in ["slow", "långsam", "sluggish", "laggy"]):
        topics.append("slow")

    # CRASHES
    if any(word in t for word in ["crash", "crashes", "crashed", "kraschar"]):
        topics.append("crash")

    # LOGIN
    if any(word in t for word in ["login", "logga in", "cannot login", "can't login"]):
        topics.append("login")

    # DEFAULT IF NOTHING DETECTED
    if not topics:
        topics = ["general"]

    # ---------- SENTIMENT ----------
    negative_words = ["slow", "crash", "error", "issue", "kraschar", "lag", "långsam"]
    sentiment = "Negative" if any(w in t for w in negative_words) else "Neutral"

    # ---------- ALERT ----------
    # Test suite expects string "Yes" or "No", NOT boolean.
    critical_words = ["slow", "bad", "Not Optimal", "Not Upto to the mark", "Not -useful" "crash", "crashes", "kraschar", "cannot login", "can't login"]
    # lowercase text for safer matching
    t_lower = t.lower()
    # condition: critical words OR negative sentiment
    if any(w.lower() in t_lower for w in critical_words) or sentiment.lower() == "negative":
        alert = "Yes"
    else:    
        alert = "No"

    return {
        "sentiment": sentiment,
        "topics": ", ".join(topics),
        "alert": alert
    }
