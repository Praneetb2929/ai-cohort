# AI System Governance, PHI/PII Security & Compliance

## 1. Data Sources & Sensitivity Levels
* **`knowledge_base.jsonl` & Plan Rules**: Public/semi-private insurance policy descriptions and benefit tiers.
* **SQLite Claims & Sessions (`coverage.db`, `conversations.db`)**: Highly sensitive Protected Health Information (PHI) and Personally Identifiable Information (PII).

## 2. PHI / PII Fields Present
* `member_id` / `session_id` (Unique personal identifiers)
* `claim_id`, `amount`, `date` (Financial and claim records)
* `procedure` / Medical queries (Individual health condition associations)

## 3. Bias Risks & Mitigation
* **Plan-Tier Bias**: Risk of assuming lower plan tiers (e.g., Bronze) imply non-compliance or inferior care. Mitigation involves standardized, neutral wording across all benefit lookups.
* **Terminology Inequity**: Providing plain-language definitions on first mention so all users understand coverage equally.

## 4. Accountability & Review
* **Designated Reviewer**: Lead Clinical Compliance Officer and Data Protection Officer (DPO).
* **Audit Cadence**: Bi-weekly automated redaction audits and human-in-the-loop spot checks of sampled logs.

> **Production Disclaimer**: Production use requires a formal compliance review beyond this exercise.