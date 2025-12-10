
# **Customer-Feedback-Analysis-Tool**

A hybrid rule-based + AI-assisted system designed to analyze customer feedback with low latency, fault tolerance, and scalable architecture. The tool processes user messages, categorizes sentiment, extracts topics, triggers alerts, and provides a lightweight UI for interaction.

To run the pipeline cmd: python run_pipeline.py

---

## **1. Design Rationale**

### **Key Questions Considered**

* Is the incoming feedback English-only, or multilingual?
* Is feedback plain text, or might it include attachments, emojis, or ratings (1–5)?
* Does feedback describe overall product experience or specific features?
* What sentiment structure is required—binary, ternary (positive/neutral/negative), or extended (e.g., mixed)?
* Are company-specific keywords needed for routing feedback (e.g., escalation to compliance)?
* Should feedback data be stored permanently or only temporarily?
* If multiple messages report a common issue, should the system auto-flag it as critical?

---

## **2. Approaches Considered**

### **All-in-One AI Model (GPT / LLM)**

**Pros**

* Minimal integration overhead
* One model for sentiment + topic detection

**Cons**

* API cost
* Possibility of latency spikes
* Caching required for performance

---

### **Hybrid (Rules + AI)**

**Pros**

* Fast responses for common keyword patterns
* AI resolves ambiguous cases

**Cons**

* More code maintenance
* Rule updates required over time

---

### **Self-Hosted Models**

**Pros**

* No external API costs
* Full control over inference

**Cons**

* Requires significant compute capacity
* Scaling and updates are manual

---

## **3. Why the Hybrid Approach Was Chosen**

The hybrid architecture balances performance, reliability, and cost.
A fully AI-powered pipeline risks violating the sub-500ms latency requirement during busy periods and introduces dependency on external provider uptime.
Self-hosted transformers offer control but require substantial compute and continuous maintenance.

Combining deterministic rules for clear cases with AI handling nuanced or ambiguous messages results in:

* Reduced latency
* Lower overall API usage
* Increased resiliency to downtime
* Stable and predictable behavior under load

---

## **4. What This Project Does *Not* Intend to Build**

To keep scope focused, the following are intentionally excluded:

* Full multilingual processing
* Advanced analytics dashboards or complete UI suites
* Complex ML training pipelines or model fine-tuning systems

---

## **5. Setup and Usage**

### **Prerequisites**

* Python **3.12+**

### **Installation Steps**

```bash
git clone https://github.com/simply-Rahul8/Customer-Feedback-Analysis-Tool.git
cd Customer-Feedback-Analysis-Tool
pip install -r requirements.txt
```

### **Environment Setup**

Create a `.env` file in the project root.

### **When Running the Application**

* Loads variables from `.env`
* Starts FastAPI backend at `localhost`
* Starts Streamlit UI at `localhost`

### **API Endpoints**

| Method | Endpoint         | Description                               |
| ------ | ---------------- | ----------------------------------------- |
| POST   | `/feedback`      | Analyze sentiment, topics, and alert flag |
| GET    | `/feedback/{id}` | Retrieve single feedback entry            |
| GET    | `/feedback`      | Retrieve all stored feedback              |

### **Fallback Logic**

1. Check **cache**
2. Apply **rules**
3. Call **AI** only if needed

---

## **6. Assumptions**

### **Known Assumptions**

* Feedback is plain text, mainly English, may include emojis
* Multiple topics per message allowed
* Alerts triggered by severe negative sentiment or critical topics
* Expected peak volume: ~100 messages/min
* Messages may be informal or short

### **Uncertain Assumptions**

* Frequency of sarcasm or slang
* Complexity of multi-topic inputs beyond rule coverage

---

## **7. Technical Decisions**

| Component         | Choice             | Rationale                                  | Alternatives                   |
| ----------------- | ------------------ | ------------------------------------------ | ------------------------------ |
| API Framework     | FastAPI            | Async, high throughput, minimal latency    | Flask, Django REST             |
| Database          | SQLite             | Lightweight and automatic for prototypes   | PostgreSQL, MongoDB            |
| AI Provider       | OpenAI GPT         | Strong sentiment + topic detection         | Local transformers, other APIs |
| Fallback Strategy | Cache → Rules → AI | Ensures reliability and minimizes cost     | Rules only                     |
| Caching           | SQLite (in-memory) | Fast, reduces repeated inference           | Redis                          |
| UI                | Streamlit          | Simple, interactive demo with history view | React, Angular                 |
| Alerts            | Inline + counter   | Meets basic requirements                   | Email, Slack                   |

---

## **8. AI Integration**

The system uses OpenAI GPT for:

* Sentiment analysis
* Topic extraction
* Alert flagging

Prompting was iteratively refined to support:

* Emojis
* Informal phrases
* Multi-topic messages
* Very short text

### **Key AI Configuration**

* **temperature = 0** to maintain deterministic output
* Normalization post-processing for topic labels and alert consistency
* Cache-first and rules-first fallback strategy

### **Edge Cases**

* **Sarcasm**: partly handled by AI + keyword rules
* **Multiple topics**: parsed into predefined list
* **Gibberish**: tagged as "unreadable"

---

### **AI Integration Table**

```
Component               | Choice / Approach                     | Notes
----------------------- | ------------------------------------- | -----------------------------------------------
AI Model                | OpenAI GPT                            | Strong emoji and nuance support
Prompt Design           | Iterative refinement                  | Ensures multi-topic handling
Non-determinism Control | Temperature=0 + normalization          | Stable output
Fallback Handling       | Cache → Rules → AI                    | Resilient to outages
Edge Case Handling      | Sarcasm, gibberish, multi-topic        | Rules complement AI results
Caching                 | SQLite in-memory                       | Faster responses and reduced API cost
```

---

## **9a. Failure Modes – Real-World Problems**

| Failure Mode           | Issue                        | Detection                       | User Impact                   | Mitigation                         |
| ---------------------- | ---------------------------- | ------------------------------- | ----------------------------- | ---------------------------------- |
| AI Downtime            | API fails / slow response    | Timeouts, fallback trigger      | Less nuanced analysis         | Use cache + rules                  |
| Misclassification      | Incorrect sentiment or topic | Manual sampling, anomaly checks | Wrong routing or false alerts | Normalization, retries             |
| Latency Spike (>500ms) | Network or load problems     | Latency logs                    | Slow responses                | Caching, async, minimized AI calls |

---

## **9b. Technical System-Level Failures**

1. **Database Locking / Write Contention**
   Mitigate with WAL mode, retry logic, or upgrading to PostgreSQL.

2. **Cache Corruption / Stale Entries**
   Add TTL and validate structure on read.

3. **API Rate Limit / Queue Backpressure**
   Use rate limiting, batching, and fallback modes.

4. **Async Task Starvation**
   Limit concurrency; use proper async clients.

5. **Unicode / Emoji Encoding Issues**
   Force UTF-8 normalization.

6. **Streamlit ↔ FastAPI Communication Errors**
   Add health checks and retries.

7. **File-System Permission or Disk Full**
   Monitor disk usage; rotate logs.

8. **Clock Drift / Time Synchronization Errors**
   Rely on NTP or cloud provider time sync.

---

## **10. Production Considerations**

### **10.1 AI Monitoring**

* Track accuracy drift
* Monitor token usage and cost
* Measure latency end-to-end

### **10.2 Observability**

* Structured logs
* Metrics and error counters
* Distributed tracing
* Failure patterns such as timeout or slow inference

### **10.3 Prompt Versioning**

* Store prompts in a versioned repository
* Tag each production inference with a prompt version
* Run A/B comparisons before updating

### **10.4 Security for External AI**

* Use environment variables or secret vaults
* Restrict outbound access
* Encrypt customer data during transit
* Sanitize inputs to avoid prompt injection

### **10.5 Scaling to 10× Load**

* Introduce message queues
* Horizontal autoscaling
* Distributed vector search
* Background workers for batch operations
* Aggressive caching

---

### **Production Considerations Summary**

| Area              | Focus Areas                                  |
| ----------------- | -------------------------------------------- |
| AI Monitoring     | Accuracy, latency, cost control              |
| Observability     | Logs, metrics, traces                        |
| Prompt Versioning | History, tagging, A/B testing                |
| Security          | API key protection, encryption, sanitization |
| Scaling           | Queues, autoscaling, caching, workers        |

