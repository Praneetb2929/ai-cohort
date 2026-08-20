# Fine-Tuning Preparation & Analysis Notes

## 1. Recurring Issues Identified in Days 10–13 Logs

1. **Inconsistent Tone & Missing Disclaimers (Fixable by Fine-Tuning)**:
   * The base model frequently omitted the standard medical disclaimer ("This is not medical advice") or fluctuated between overly robotic and overly conversational tones. Fine-tuning reliably anchors stylistic patterns, formatting constraints, and obligatory compliance disclosures directly into model weights.
2. **Failure to Define Core Insurance Terminology (Fixable by Fine-Tuning)**:
   * Terms such as "deductible", "copay", and "coinsurance" were used without explanation. Fine-tuning ensures terms are defined consistently on first use (e.g., explaining that a deductible is the amount a member pays before insurance kicks in).
3. **Out-of-Date Coverage Facts & Missed Policy Clauses (Retrieval Problem — Not Fixable by FT)**:
   * Hallucinations or incorrect policy details occurred when relevant context chunks were not returned by semantic search. Fine-tuning cannot fix retrieval misses; dynamic real-time policy rules, deductible balances, and real-time claim numbers must be retrieved via RAG / SQL tools.

## 2. Fine-Tuning vs. Retrieval Strategy
* **Fine-Tuning Role**: Teaches *how* to answer (tone, compliance formatting, jargon definitions, strict refusal of clinical medical advice).
* **Retrieval Role**: Teaches *what* to answer (dynamic plan benefits, copay amounts, live claim statuses, and exact policy documentation).