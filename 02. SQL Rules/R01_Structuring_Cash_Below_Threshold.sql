-- R01_Structuring_Cash_Below_Threshold.sql
-- Purpose : Detect possible structuring: repeated cash deposits just under ₹50,000.
-- Logic   : 3 or more cash deposits of ₹40,000-49,999 into one account within any 10-day window.
-- Dialect : SQLite. Thresholds are illustrative for this learning project, not regulatory advice.

WITH cash AS (
    SELECT AccountID, TxnID, TxnDate, Amount
    FROM Transactions
    WHERE Channel = 'Cash Deposit' AND Direction = 'Credit' AND Amount BETWEEN 40000 AND 49999
),
win AS (
    SELECT c1.AccountID, c1.TxnDate AS window_start,
           COUNT(*) AS deposits_in_10_days, SUM(c2.Amount) AS total_inr
    FROM cash c1
    JOIN cash c2 ON c2.AccountID = c1.AccountID
                AND c2.TxnDate BETWEEN c1.TxnDate AND date(c1.TxnDate, '+9 days')
    GROUP BY c1.AccountID, c1.TxnID, c1.TxnDate
)
SELECT a.CustomerID, w.AccountID, MIN(w.window_start) AS first_window,
       MAX(w.deposits_in_10_days) AS max_deposits_in_10_days, ROUND(MAX(w.total_inr), 0) AS max_10_day_total_inr
FROM win w JOIN Accounts a ON a.AccountID = w.AccountID
WHERE w.deposits_in_10_days >= 3
GROUP BY a.CustomerID, w.AccountID
ORDER BY max_10_day_total_inr DESC;
