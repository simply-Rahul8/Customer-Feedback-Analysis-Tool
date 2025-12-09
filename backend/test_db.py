from backend.models import Feedback
from backend.main import SessionLocal

db = SessionLocal()
new_feedback = Feedback(
    text="This product is great!",
    sentiment="positive",
    topics="product quality",
    alert="no"
)
db.add(new_feedback)
db.commit()

# Fetch
all_feedback = db.query(Feedback).all()
for f in all_feedback:
    print(f.id, f.text, f.sentiment, f.topics, f.alert)

db.close()
