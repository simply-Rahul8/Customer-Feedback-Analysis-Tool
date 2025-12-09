from backend.llm_client import analyze_feedback

feedback = "I love the new app update, but the login is slow."
result = analyze_feedback(feedback)
print(result)
