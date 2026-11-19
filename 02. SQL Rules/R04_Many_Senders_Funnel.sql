-- R04_Many_Senders_Funnel.sql
-- Purpose : Detect funnel accounts: many different people paying in over a short period.
-- Logic   : 15 or more distinct counterparties crediting one account within any 7-day window.
-- Dialect : SQLite. Thresholds are illustrative for this learning project, not regulatory advice.

WITH cr AS (
    SELECT AccountID, TxnDate, Counterparty FROM Transactions WHERE Direction = 'Credit'
),
win AS (
    SELECT c1.AccountID, c1.TxnDate AS window_start, COUNT(DISTINCT c2.Counterparty) AS senders
    FROM (SELECT DISTINCT AccountID, TxnDate FROM cr) c1
    JOIN cr c2 ON c2.AccountID = c1.AccountID AND c2.TxnDate BETWEEN c1.TxnDate AND date(c1.TxnDate, '+6 days')
    GROUP BY c1.AccountID, c1.TxnDate
)
SELECT a.CustomerID, w.AccountID, MAX(w.senders) AS max_senders_in_7_days, MIN(w.window_start) AS first_window
FROM win w JOIN Accounts a ON a.AccountID = w.AccountID
WHERE w.senders >= 15
GROUP BY a.CustomerID, w.AccountID
ORDER BY max_senders_in_7_days DESC;
