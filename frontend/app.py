# app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv
# FastAPI backend URL

load_dotenv()
API_URL = os.getenv("API_URL")

st.title("Customer Feedback Analysis Tool")

# Input box for new feedback
feedback_text = st.text_area("Enter customer feedback (text + emojis allowed):", height=100)

if st.button("Submit Feedback"):
    if feedback_text.strip() == "":
        st.warning("Please enter some feedback before submitting.")
    else:
        try:
            response = requests.post(
                f"{API_URL}/feedback",
                json={"text": feedback_text}
            )
            if response.status_code == 200:
                result = response.json()
                st.success("Feedback submitted and analyzed!")
                st.write("**Sentiment:**", result["sentiment"])
                st.write("**Topics:**", result["topics"])
                st.write("**Alert:**", result["alert"])

                # ✅ Show popup/modal if alert is Yes
                if result["alert"].lower() == "yes":
                    st.warning("🚨 Alert")
                    st.toast("🚨 Alert sent to consent team")



            else:
                st.error("Failed to submit feedback: " + response.text)
        except Exception as e:
            st.error("Error connecting to backend: " + str(e))

# Display last 2 feedbacks
#st.subheader("Recent Feedback (Last 2)")
#try:
#    recent = requests.get(f"{API_URL}/feedback/recent").json()
#    for f in recent:
#        # One-line history style
#        st.write(f"{f['text']} → [Sentiment: {f['sentiment']}, Topics: {f['topics']}, Alert: {f['alert']}]")
#except Exception as e:
#    st.error("Could not fetch recent feedback: " + str(e))
