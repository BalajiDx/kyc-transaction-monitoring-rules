# Investigation Report - ALT-0040

> Synthetic learning case built from the generated data. Not a real customer.

| Field | Value |
|---|---|
| Alert | ALT-0040 · priority **P3 - review and close** · score 45 |
| Customer | K00564 · Business Owner · Individual · Tamil Nadu |
| Risk rating / PEP | High / No |
| Declared income | ₹1,769,000 a year |
| 2024 activity | 188 transactions · credits ₹1,743,811 · debits ₹1,173,292 |
| Rules hit | R04 |

## Rule hits
| Rule | First seen | Detail | Value (₹) |
|---|---|---|---|
| R04 15+ different senders in 7 days | 2024-01-01 | 27 senders in 7 days | 104,101 |

## Key transactions
| Date | Txn | Channel | Direction | Amount (₹) | Counterparty |
|---|---|---|---|---|---|
| 2024-01-01 | TX0000238 | UPI | Credit | 471 | CPS55514 |
| 2024-01-01 | TX0000239 | UPI | Credit | 2,493 | CPS13181 |
| 2024-01-02 | TX0000996 | UPI | Credit | 166 | CPS03800 |
| 2024-01-02 | TX0000997 | UPI | Credit | 1,467 | CPS16222 |
| 2024-01-02 | TX0000998 | UPI | Credit | 2,190 | CPS81592 |
| 2024-01-02 | TX0000999 | UPI | Credit | 1,126 | CPS26337 |
| 2024-01-03 | TX0001764 | UPI | Credit | 2,141 | CPS83513 |
| 2024-01-03 | TX0001765 | UPI | Credit | 1,909 | CPS22046 |
| 2024-01-04 | TX0002522 | UPI | Credit | 1,716 | CPS79417 |
| 2024-01-04 | TX0002523 | UPI | Credit | 1,025 | CPS77841 |

## Assessment
The 10+ credits are small UPI payments (166-2,493 each) from many different payers, typical of a
retail shop. The customer is **Business Owner**, the amounts match the declared business and money is not moved straight out.

## Decision
**Closed: false positive (legitimate merchant receipts).** No STR. Recommend tagging the account as a verified merchant
so R04 uses a higher threshold for it (see Rule Catalog, tuning note 2).
