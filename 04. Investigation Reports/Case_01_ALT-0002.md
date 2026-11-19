# Investigation Report - ALT-0002

> Synthetic learning case built from the generated data. Not a real customer.

| Field | Value |
|---|---|
| Alert | ALT-0002 · priority **P1 - investigate within 2 days** · score 84 |
| Customer | K00018 · Self-Employed · Individual · Puducherry |
| Risk rating / PEP | Medium / No |
| Declared income | ₹797,000 a year |
| 2024 activity | 137 transactions · credits ₹3,866,597 · debits ₹3,503,621 |
| Rules hit | R02, R03, R06 |

## Rule hits
| Rule | First seen | Detail | Value (₹) |
|---|---|---|---|
| R02 Large credit moved out within 2 days | 2024-07-09 | 3 credit(s) moved out within 2 days | 3,096,348 |
| R03 Credits above 3x declared income | 2024-01-07 | credits 4.9x declared income | 3,866,597 |
| R06 Monthly credits above 5x own normal | 2024-07-01 | 2024-07 credits 7x the customer's normal month | 1,530,522 |
| R06 Monthly credits above 5x own normal | 2024-08-01 | 2024-08 credits 9x the customer's normal month | 1,694,760 |

## Key transactions
| Date | Txn | Channel | Direction | Amount (₹) | Counterparty |
|---|---|---|---|---|---|
| 2024-07-09 | TX0102793 | RTGS | Credit | 1,451,974 | CP02374 |
| 2024-07-09 | TX0102794 | RTGS | Debit | 1,366,706 | CP00063 |
| 2024-08-07 | TX0117888 | RTGS | Credit | 973,480 | CP02244 |
| 2024-08-07 | TX0117889 | RTGS | Debit | 937,655 | CP02450 |
| 2024-08-16 | TX0122768 | RTGS | Credit | 670,894 | CP02130 |
| 2024-08-16 | TX0122769 | RTGS | Debit | 642,446 | CP02364 |

## Assessment
- Activity is **inconsistent with the profile**: declared income ₹797,000 a year, but 2024 credits total ₹3,866,597
  (4.9x).
- The pattern matches the **Income mismatch; Pass-through (rapid in/out); Unusual spike** typology flagged by the rules above.
- Customer risk rating **Medium**; KYC last reviewed 2021-10-17.

## Recommended actions
1. Request source-of-funds documents and an explanation for the flagged transactions.
2. Bring forward the periodic KYC review and update the declared income and occupation.
3. If no satisfactory explanation within the review period, **escalate to the Principal Officer to consider an STR** (the
   suspicious transaction report filed with FIU-IND in India).
4. Place the account on enhanced monitoring for 6 months.

## Decision
**Escalate** (synthetic case; outcome shown for illustration).
