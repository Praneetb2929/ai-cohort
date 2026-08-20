# Retrieval Test Harness Results

| # | Question Text | Classification | Retrieved Context Excerpt | Manual Score |
|---|---|---|---|---|
| 1 | What is my copay for primary care? | Structured (SQL) | Primary care visit copay: $20 for Gold, $35 for Silver | good |
| 2 | Is maternity care covered on the Bronze plan? | Unstructured (Vector) | Bronze policy: Maternity care is covered after meeting annual deductible. | good |
| 3 | What is the status of claim C-2031? | Structured (SQL) | Claim C-2031: Status = Processing, Amount = $450 | good |
| 4 | Are cosmetic surgeries excluded under standard coverage? | Unstructured (Vector) | Policy exclusions: Cosmetic and elective procedures are strictly excluded. | good |
| 5 | What is the out-of-pocket maximum for the Gold plan? | Structured (SQL) | Out-of-pocket maximum: $4,000 individual / $8,000 family | good |
| 6 | How do I submit an out-of-network reimbursement claim? | Unstructured (Vector) | Claims process: Submit claim form along with itemized receipt within 90 days. | good |
| 7 | What is the copay and coverage rule for emergency room visits on Gold? | Hybrid (SQL + Vector) | Copay: $150. Context: Emergency services covered worldwide without prior auth. | good |
| 8 | What is the annual deductible for individual coverage in Bronze? | Structured (SQL) | Bronze deductible: $6,500 individual | good |
| 9 | Is acupuncture covered under alternative therapy benefits? | Unstructured (Vector) | Covered services: Acupuncture is covered up to 12 visits per calendar year. | good |
| 10 | What is the status and coverage policy for claim C-9821 regarding MRI scans? | Hybrid (SQL + Vector) | Claim C-9821: Approved. Policy: High-tech imaging covered with 20% coinsurance. | good |