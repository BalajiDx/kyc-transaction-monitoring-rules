# Rule Catalog

Six transaction-monitoring rules plus three KYC checks. Each rule exists twice, as SQL (`02. SQL Rules/`) and in
`03. Python Rules Engine/rules_engine.py`, and both give the same customers. Thresholds are **illustrative**, chosen for this synthetic
learning project; real thresholds come from a bank's risk assessment and regulator guidance.

## Monitoring rules and how they performed
"Recall" = planted cases of that typology the rule caught. "Precision" = share of flagged customers who are any planted case
(the rest are legitimate look-alikes, that is, false positives).

| ID | Rule | Typology | Threshold | Customers flagged | Recall | Precision |
|---|---|---|---|---|---|---|
| R01 | Cash deposits just under ₹50,000 | Structuring | ≥3 cash deposits of ₹40,000-49,999 in any 10-day window | 23 | 79% | 48% |
| R02 | Large credit moved out within 2 days | Pass-through (rapid in/out) | credit ≥ ₹2 lakh and a debit of 90-100% of it within 2 days | 28 | 100% | 43% |
| R03 | Credits above 3x declared income | Income mismatch | 2024 credits > 3x declared annual income and > ₹5 lakh | 43 | 100% | 63% |
| R04 | 15+ different senders in 7 days | Funnel account (many senders) | ≥15 distinct senders crediting one account in any 7-day window | 30 | 100% | 27% |
| R05 | Transfer with high-risk jurisdiction | High-risk jurisdiction | any transfer to/from a listed high-risk jurisdiction | 7 | 100% | 100% |
| R06 | Monthly credits above 5x own normal | Unusual spike | month's credits > 5x the customer's average of other months and > ₹3 lakh | 53 | n/a | 68% |

Overall: **98 customers alerted, 48 of 51 planted cases caught (94%)**, and
49% of alerts are true cases. R06 has no planted typology of its own; it is a behaviour-change rule that backs up the others.

## Rule details
### R01 - Cash deposits just under ₹50,000
- **Typology:** Structuring
- **Why it matters:** Breaking cash into amounts below the ₹50,000 PAN-quoting level to avoid reporting.
- **Logic:** ≥3 cash deposits of ₹40,000-49,999 in any 10-day window
- **Typical false positives:** Cash businesses depositing daily takings.
- **Files:** `02. SQL Rules/R01_Structuring_Cash_Below_Threshold.sql`, function block `R01` in `rules_engine.py`

### R02 - Large credit moved out within 2 days
- **Typology:** Pass-through (rapid in/out)
- **Why it matters:** Account used as a conduit: money arrives and leaves before it can be questioned.
- **Logic:** credit ≥ ₹2 lakh and a debit of 90-100% of it within 2 days
- **Typical false positives:** Property purchase, FD maturity paid to a builder, loan disbursement passed to a dealer.
- **Files:** `02. SQL Rules/R02_Rapid_Pass_Through.sql`, function block `R02` in `rules_engine.py`

### R03 - Credits above 3x declared income
- **Typology:** Income mismatch
- **Why it matters:** Activity inconsistent with the customer's declared profile (for example a student receiving lakhs).
- **Logic:** 2024 credits > 3x declared annual income and > ₹5 lakh
- **Typical false positives:** Asset sales, inheritance, stale declared income. Refresh income at periodic KYC.
- **Files:** `02. SQL Rules/R03_Income_Mismatch.sql`, function block `R03` in `rules_engine.py`

### R04 - 15+ different senders in 7 days
- **Typology:** Funnel account (many senders)
- **Why it matters:** Mule or collection account gathering many small payments.
- **Logic:** ≥15 distinct senders crediting one account in any 7-day window
- **Typical false positives:** Shops and small merchants paid over UPI. Exclude verified merchant accounts or raise the threshold for them.
- **Files:** `02. SQL Rules/R04_Many_Senders_Funnel.sql`, function block `R04` in `rules_engine.py`

### R05 - Transfer with high-risk jurisdiction
- **Typology:** High-risk jurisdiction
- **Why it matters:** Exposure to jurisdictions on the bank's high-risk list.
- **Logic:** any transfer to/from a listed high-risk jurisdiction
- **Typical false positives:** Legitimate trade or family remittances. Usually still reviewed.
- **Files:** `02. SQL Rules/R05_High_Risk_Jurisdiction.sql`, function block `R05` in `rules_engine.py`

### R06 - Monthly credits above 5x own normal
- **Typology:** Unusual spike
- **Why it matters:** Sudden change against the customer's own history, independent of fixed amounts.
- **Logic:** month's credits > 5x the customer's average of other months and > ₹3 lakh
- **Typical false positives:** One-off events (bonus, property sale); low base months.
- **Files:** `02. SQL Rules/R06_Monthly_Spike_vs_Own_History.sql`, function block `R06` in `rules_engine.py`

## KYC checks
| ID | Check | Logic |
|---|---|---|
| K01 | Document completeness | PAN, Aadhaar verification and address proof all present |
| K02 | Periodic review overdue | High risk every 2 years, Medium every 8, Low every 10 (cycle used for this exercise) |
| K03 | High risk without EDD | RiskRating = High and EDDCompleted = 0 |

## Alert scoring
`score = sum of rule weights x customer-risk multiplier (+20 if PEP)`, capped at 100.
Weights: R05 40, R02 35, R01 30, R04 30, R03 20, R06 15. Multiplier: High 1.5, Medium 1.2, Low 1.0.
Priority: **P1** ≥ 80 (investigate within 2 days), **P2** 50-79 (within 7 days), **P3** < 50 (review and close).

## Tuning notes (what the results suggest)
1. **R01 misses evasive structuring** (3 of 14 planted cases spread deposits over more than 10 days). A 30-day window or a monthly count of near-threshold deposits would catch them, at the cost of more alerts on cash businesses.
2. **R04 is noisy** (27% precision) because shops receive many UPI payments. Segmenting by customer type (exclude verified merchants) is the obvious fix.
3. **R02 and R03 flag one-off property transactions.** Asking for a source-of-funds document closes these quickly; they should not be tuned out because pass-through is high risk.
4. Rules that fire **together** are far more likely to be real: see the priority mix in `Alerts.csv`.
