# One-Page Experiment Design: Prompt Variant A vs. Variant E

## 1. Experiment Overview & Objective
Evaluate whether the Hybrid Prompt (Variant E with chain-of-thought verification and structured disclaimers) outperforms the Strict Formal Prompt (Variant A) in answer accuracy, policy compliance, and reduction of hallucinations.

## 2. Hypothesis
**Hypothesis**: Variant E will yield a statistically significant increase in compliant, grounded responses (≥90% rated "good") compared to Variant A by validating plan type and section metadata before answering.

## 3. Core Evaluation Metrics
* **Primary Metric**: Percentage of answers rated "good" (1–5 scale, threshold ≥ 4).
* **Secondary Metrics**:
  * Compliance Score (% of answers containing non-medical advice disclaimer).
  * Average Output Token Count (conciseness vs. informativeness).
  * Latency (Time to First Token & Full Response Time).

## 4. Sample Size & Decision Rule
* **Sample Size**: 15 distinct domain test questions covering structured copays, policy exclusions, claims status, and ambiguous benefits.
* **Decision Rule**: Variant E will be deployed to production if it beats Variant A by at least 15% on the primary compliance metric without increasing token cost by more than 25%.