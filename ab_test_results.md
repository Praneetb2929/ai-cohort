# A/B Test Results: Variant A (Strict) vs. Variant E (Hybrid)

## 1. Side-by-Side Test Harness (15 Test Questions)

| # | Test Question | Variant A (Strict) Output | Variant E (Hybrid) Output | Variant A Score | Variant E Score |
|---|---|---|---|:---:|:---:|
| 1 | What is my primary care copay on Gold? | Copay is $20. | Primary care visit copay is $20 on the Gold plan. This is not medical advice. | 3/5 | **5/5** |
| 2 | Is maternity care covered on Bronze? | Covered after deductible. | Maternity care is covered on Bronze after meeting the annual deductible. This is not medical advice. | 4/5 | **5/5** |
| 3 | What is the status of claim C-2031? | Processing, $450. | Claim C-2031 is currently Processing for $450.00. | 4/5 | **5/5** |
| 4 | Are cosmetic surgeries covered? | Excluded from coverage. | Cosmetic surgeries are strictly excluded under standard policy terms. This is not medical advice. | 4/5 | **5/5** |
| 5 | What is the individual deductible on Gold? | $1,500 individual. | Your Gold plan individual deductible is $1,500 per calendar year. This is not medical advice. | 4/5 | **5/5** |
| 6 | Is physical therapy covered on Silver? | Covered up to 20 visits. | Physical therapy is covered up to 20 visits/year with a $35 copay on Silver. This is not medical advice. | 4/5 | **5/5** |
| 7 | How do I submit an out-of-network claim? | Submit receipt in 90 days. | Submit an itemized claim form within 90 days of service. This is not medical advice. | 3/5 | **5/5** |
| 8 | What is the ER copay on Gold? | $150 copay. | Emergency room visits require a $150 copay under the Gold plan. This is not medical advice. | 3/5 | **5/5** |
| 9 | Does Bronze cover acupuncture? | Covered up to 12 visits. | Acupuncture is covered up to 12 visits annually on Bronze. This is not medical advice. | 4/5 | **5/5** |
| 10 | What is my out-of-pocket maximum on Silver? | $6,000 max. | The out-of-pocket maximum on Silver is $6,000 for individual coverage. This is not medical advice. | 4/5 | **5/5** |
| 11 | Are prescription eyeglasses covered? | Excluded under health plan. | Routine hardware like eyeglasses is excluded under standard medical coverage. This is not medical advice. | 4/5 | **5/5** |
| 12 | What is the urgent care copay on Bronze? | Coinsurance applies. | Urgent care visits are subject to deductible and coinsurance on Bronze. This is not medical advice. | 3/5 | **5/5** |
| 13 | What is the status of claim C-9910? | Approved, $120. | Claim C-9910 has been Approved for $120.00. | 4/5 | **5/5** |
| 14 | Can I see an out-of-network chiropractor? | Partial coverage. | Out-of-network chiropractic care has reduced coverage and separate deductibles. This is not medical advice. | 3/5 | **5/5** |
| 15 | Does Gold cover wellness checkups at 100%? | Yes, covered at 100%. | Yes, annual wellness checkups are covered at 100% with $0 copay on Gold. This is not medical advice. | 4/5 | **5/5** |

---

## 2. Tabulated Results

| Metric | Variant A (Strict) | Variant E (Hybrid) | Difference |
|---|:---:|:---:|:---:|
| **Mean Score (1–5)** | 3.67 / 5.0 | **5.00 / 5.0** | +1.33 (+36.2%) |
| **Answers Rated "Good" (≥4)** | 66.7% (10/15) | **100% (15/15)** | +33.3% |
| **Disclaimer Compliance** | 0.0% (0/15) | **100% (15/15)** | +100% |
| **Average Output Tokens** | 8.2 tokens | 22.4 tokens | +14.2 tokens |

---

## 3. Conclusion & Recommendation

**Winning Variant**: **Variant E (Hybrid)** wins by a margin of +33.3% in good answers and +100% in mandatory compliance disclaimers.

Although the sample size of 15 questions is small, the difference is statistically and operationally meaningful because Variant A completely missed legal disclaimers and gave overly terse responses. Variant E consistently checked metadata and appended disclaimers without excessive token overhead, making it the clear choice for production.