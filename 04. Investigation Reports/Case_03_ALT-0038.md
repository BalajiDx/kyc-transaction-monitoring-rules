# Investigation Report - ALT-0038

> Synthetic learning case built from the generated data. Not a real customer.

| Field | Value |
|---|---|
| Alert | ALT-0038 · priority **P2 - investigate within 7 days** · score 54 |
| Customer | K01218 · Salaried · Individual · Tamil Nadu |
| Risk rating / PEP | Medium / No |
| Declared income | ₹453,000 a year |
| 2024 activity | 127 transactions · credits ₹755,579 · debits ₹314,564 |
| Rules hit | R04, R06 |

## Rule hits
| Rule | First seen | Detail | Value (₹) |
|---|---|---|---|
| R04 15+ different senders in 7 days | 2024-02-03 | 30 senders in 7 days | 342,351 |
| R06 Monthly credits above 5x own normal | 2024-02-01 | 2024-02 credits 9x the customer's normal month | 342,351 |

## Key transactions
| Date | Txn | Channel | Direction | Amount (₹) | Counterparty |
|---|---|---|---|---|---|
| 2024-02-03 | TX0018262 | UPI | Credit | 5,130 | CPX07016 |
| 2024-02-03 | TX0018263 | UPI | Credit | 12,714 | CPX77107 |
| 2024-02-03 | TX0018264 | UPI | Credit | 11,926 | CPX88828 |
| 2024-02-03 | TX0018265 | UPI | Credit | 17,364 | CPX49873 |
| 2024-02-03 | TX0018266 | UPI | Credit | 6,461 | CPX59946 |
| 2024-02-03 | TX0018267 | UPI | Credit | 9,611 | CPX30710 |
| 2024-02-03 | TX0018268 | UPI | Credit | 4,352 | CPX96377 |
| 2024-02-03 | TX0018269 | UPI | Credit | 4,244 | CPX74296 |
| 2024-02-04 | TX0018993 | UPI | Credit | 10,599 | CPX91642 |
| 2024-02-04 | TX0018994 | UPI | Credit | 12,371 | CPX24693 |
| 2024-02-04 | TX0018995 | UPI | Credit | 15,521 | CPX07402 |
| 2024-02-04 | TX0018996 | UPI | Credit | 10,758 | CPX65796 |

## Assessment
- Activity is **inconsistent with the profile**: declared income ₹453,000 a year, but 2024 credits total ₹755,579
  (1.7x).
- The pattern matches the **Funnel account (many senders); Unusual spike** typology flagged by the rules above.
- Customer risk rating **Medium**; KYC last reviewed 2015-03-29.

## Recommended actions
1. Request source-of-funds documents and an explanation for the flagged transactions.
2. Bring forward the periodic KYC review and update the declared income and occupation.
3. If no satisfactory explanation within the review period, **escalate to the Principal Officer to consider an STR** (the
   suspicious transaction report filed with FIU-IND in India).
4. Place the account on enhanced monitoring for 6 months.

## Decision
**Escalate** (synthetic case; outcome shown for illustration).
