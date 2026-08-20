# Base Model vs. Fine-Tuned Model Evaluation Report

## 1. Evaluation Setup & Test Methodology
We evaluate the 5 held-out test questions from `fine_tune_test.jsonl` across two model variants:
* **Base Model**: Pretrained LLM with standard system prompt.
* **Fine-Tuned Model**: PEFT / LoRA fine-tuned checkpoint trained on the 25 domain-specific Q&A pairs.

Scoring criteria (1–5 scale):
* **Tone**: Empathetic, calm, professional tone suitable for healthcare members.
* **Correctness**: Accurate facts matching the plan rules and context.
* **Disclaimer Usage**: Explicit adherence to compliance disclaimers ("This is not medical advice").
* **Terminology Clarity**: Explaining terms like "deductible", "coinsurance", and "copay" in plain language on first mention.

---

## 2. Side-by-Side Test Comparison

### Question 1: "What is a specialist copay on Silver?"
* **Base Model**: "A specialist copay on the Silver plan is $50."
  * Scores: Tone: 3/5 | Correctness: 5/5 | Disclaimer: 1/5 | Terminology Clarity: 2/5
* **Fine-Tuned Model**: "A specialist copay is a predetermined flat fee paid when visiting a specialist physician. On the Silver plan, this copay is $50 per visit. This is not medical advice."
  * Scores: Tone: 5/5 | Correctness: 5/5 | Disclaimer: 5/5 | Terminology Clarity: 5/5

### Question 2: "Is elective weight-loss surgery covered?"
* **Base Model**: "No, elective weight-loss surgery usually isn't covered unless it is medically necessary."
  * Scores: Tone: 3/5 | Correctness: 4/5 | Disclaimer: 1/5 | Terminology Clarity: 3/5
* **Fine-Tuned Model**: "Elective bariatric or weight-loss procedures require prior authorization and documented clinical necessity review before coverage is approved. This is not medical advice."
  * Scores: Tone: 5/5 | Correctness: 5/5 | Disclaimer: 5/5 | Terminology Clarity: 5/5

### Question 3: "What is an open enrollment period?"
* **Base Model**: "Open enrollment is when you sign up for health insurance every year."
  * Scores: Tone: 3/5 | Correctness: 4/5 | Disclaimer: 1/5 | Terminology Clarity: 3/5
* **Fine-Tuned Model**: "Open enrollment is the designated annual window during which members can sign up for, switch, or adjust their health insurance plan benefits. This is not medical advice."
  * Scores: Tone: 5/5 | Correctness: 5/5 | Disclaimer: 5/5 | Terminology Clarity: 5/5

### Question 4: "How are ambulance transports billed?"
* **Base Model**: "Ambulance rides are billed with a 15% coinsurance after your deductible."
  * Scores: Tone: 3/5 | Correctness: 5/5 | Disclaimer: 1/5 | Terminology Clarity: 2/5
* **Fine-Tuned Model**: "Emergency ground ambulance rides are billed with a 15% coinsurance after you meet your deductible. Coinsurance is your percentage share of covered costs. This is not medical advice."
  * Scores: Tone: 5/5 | Correctness: 5/5 | Disclaimer: 5/5 | Terminology Clarity: 5/5

### Question 5: "What is the Bronze family deductible?"
* **Base Model**: "The Bronze family deductible is $13,000 per policy year."
  * Scores: Tone: 3/5 | Correctness: 5/5 | Disclaimer: 1/5 | Terminology Clarity: 2/5
* **Fine-Tuned Model**: "A deductible is the total amount a family pays out-of-pocket before insurance coverage begins. For the Bronze plan, the family deductible is $13,000 per policy year. This is not medical advice."
  * Scores: Tone: 5/5 | Correctness: 5/5 | Disclaimer: 5/5 | Terminology Clarity: 5/5

---

## 3. Aggregate Score Summary

| Metric | Base Model Average | Fine-Tuned Model Average |
|---|:---:|:---:|
| **Tone** | 3.0 / 5 | **5.0 / 5** |
| **Correctness** | 4.6 / 5 | **5.0 / 5** |
| **Disclaimer Usage** | 1.0 / 5 | **5.0 / 5** |
| **Terminology Clarity** | 2.4 / 5 | **5.0 / 5** |

---

## 4. Conclusion

* **Consistency Improvements**: Fine-tuning with LoRA meaningfully improved structural consistency, achieving 100% adherence to required compliance disclaimers and consistently clarifying insurance terminology for non-expert members.
* **Fine-Tuning vs. Retrieval & Prompt Tuning**: Prompt engineering alone can guide tone, but fine-tuning hardwires stylistic constraints and reduces system prompt token overhead. However, factual accuracy regarding dynamic plan rules and claim states still fundamentally relies on retrieval (RAG). The combination of a fine-tuned model for tone/format with RAG for real-time data delivers optimal production performance.