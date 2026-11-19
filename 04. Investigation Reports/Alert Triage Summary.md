# Alert Triage Summary

98 customer alerts from `rules_engine.py`, by priority. "True cases" are customers that appear in the planted scenarios.

| Priority | Alerts | True cases | Hit rate |
|---|---|---|---|
| P1 - investigate within 2 days | 12 | 7 | 58% |
| P2 - investigate within 7 days | 26 | 15 | 58% |
| P3 - review and close | 60 | 26 | 43% |

Higher priorities are far more likely to be real, so working the queue in priority order finds most true cases first.

## Sample case files
| File | Typology | Outcome |
|---|---|---|
| Case_01_ALT-0002.md | Income mismatch; Pass-through (rapid in/out); Unusual spike | Escalate |
| Case_02_ALT-0034.md | Structuring; Unusual spike | Escalate |
| Case_03_ALT-0038.md | Funnel account (many senders); Unusual spike | Escalate |
| Case_04_ALT-0040_False_Positive.md | Funnel account (many senders) | Closed, false positive |
