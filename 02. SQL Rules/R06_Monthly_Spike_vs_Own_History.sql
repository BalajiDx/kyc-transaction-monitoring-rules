-- R06_Monthly_Spike_vs_Own_History.sql
-- Purpose : Detect sudden spikes: a month's credits far above the customer's own normal.
-- Logic   : Monthly credits > 5x the customer's average month (excluding that month) and > ₹3 lakh.
-- Dialect : SQLite. Thresholds are illustrative for this learning project, not regulatory advice.

WITH m AS (
    SELECT a.CustomerID, strftime('%Y-%m', t.TxnDate) AS month, SUM(t.Amount) AS credits
    FROM Transactions t JOIN Accounts a ON a.AccountID = t.AccountID
    WHERE t.Direction = 'Credit'
    GROUP BY a.CustomerID, 2
),
x AS (
    SELECT CustomerID, month, credits,
           (SUM(credits) OVER (PARTITION BY CustomerID) - credits) / NULLIF(COUNT(*) OVER (PARTITION BY CustomerID) - 1, 0) AS avg_other_months
    FROM m
)
SELECT CustomerID, month, ROUND(credits, 0) AS credits_inr, ROUND(avg_other_months, 0) AS avg_other_months_inr,
       ROUND(credits / avg_other_months, 1) AS times_normal
FROM x
WHERE credits > 5 * avg_other_months AND credits > 300000
ORDER BY times_normal DESC;
