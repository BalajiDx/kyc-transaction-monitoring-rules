# Investigation Report - ALT-0034

> Synthetic learning case built from the generated data. Not a real customer.

| Field | Value |
|---|---|
| Alert | ALT-0034 · priority **P2 - investigate within 7 days** · score 68 |
| Customer | K00648 · Business Owner · Individual · Tamil Nadu |
| Risk rating / PEP | High / No |
| Declared income | ₹601,000 a year |
| 2024 activity | 145 transactions · credits ₹794,009 · debits ₹436,321 |
| Rules hit | R01, R06 |

## Rule hits
| Rule | First seen | Detail | Value (₹) |
|---|---|---|---|
| R01 Cash deposits just under ₹50,000 | 2024-05-19 | 6 deposits of ₹40-50k in 10 days | 288,417 |
| R06 Monthly credits above 5x own normal | 2024-05-01 | 2024-05 credits 7x the customer's normal month | 315,965 |

## Key transactions
| Date | Txn | Channel | Direction | Amount (₹) | Counterparty |
|---|---|---|---|---|---|
| 2024-01-01 | TX0000271 | Cash Deposit | Credit | 15,846 | CP01071 |
| 2024-01-04 | TX0002568 | Cash Deposit | Credit | 5,958 | CP01765 |
| 2024-03-11 | TX0039293 | Cash Deposit | Credit | 10,801 | CP01202 |
| 2024-03-17 | TX0042491 | Cash Deposit | Credit | 6,900 | CP00303 |
| 2024-05-19 | TX0075854 | Cash Deposit | Credit | 49,898 | Branch cash |
| 2024-05-20 | TX0076424 | Cash Deposit | Credit | 47,668 | Branch cash |
| 2024-05-22 | TX0077534 | Cash Deposit | Credit | 48,402 | Branch cash |
| 2024-05-23 | TX0078092 | Cash Deposit | Credit | 45,715 | Branch cash |
| 2024-05-25 | TX0079169 | Cash Deposit | Credit | 47,219 | Branch cash |
| 2024-05-26 | TX0079732 | Cash Deposit | Credit | 49,515 | Branch cash |
| 2024-06-07 | TX0085647 | Cash Deposit | Credit | 6,704 | CP01985 |
| 2024-07-18 | TX0107876 | Cash Deposit | Credit | 16,123 | CP01442 |

## Assessment
- Activity is **inconsistent with the profile**: declared income ₹601,000 a year, but 2024 credits total ₹794,009
  (1.3x).
- The pattern matches the **Structuring; Unusual spike** typology flagged by the rules above.
- Customer risk rating **High**; KYC last reviewed 2022-07-16.

## Recommended actions
1. Request source-of-funds documents and an explanation for the flagged transactions.
2. Bring forward the periodic KYC review and update the declared income and occupation.
3. If no satisfactory explanation within the review period, **escalate to the Principal Officer to consider an STR** (the
   suspicious transaction report filed with FIU-IND in India).
4. Place the account on enhanced monitoring for 6 months.

## Decision
**Escalate** (synthetic case; outcome shown for illustration).
