-- R02_Rapid_Pass_Through.sql
-- Purpose : Detect pass-through activity: large credits moved out almost immediately.
-- Logic   : Credit of ₹2 lakh or more followed within 2 days by a debit of 90-100% of that amount.
-- Dialect : SQLite. Thresholds are illustrative for this learning project, not regulatory advice.

SELECT a.CustomerID, cr.AccountID,
       COUNT(DISTINCT cr.TxnID)   AS pass_through_pairs,
       ROUND(SUM(cr.Amount), 0)   AS credited_inr,
       MIN(cr.TxnDate)            AS first_seen
FROM Transactions cr
JOIN Transactions db ON db.AccountID = cr.AccountID
                    AND db.Direction = 'Debit'
                    AND db.TxnDate BETWEEN cr.TxnDate AND date(cr.TxnDate, '+2 days')
                    AND db.Amount BETWEEN 0.9 * cr.Amount AND cr.Amount
JOIN Accounts a ON a.AccountID = cr.AccountID
WHERE cr.Direction = 'Credit' AND cr.Amount >= 200000
GROUP BY a.CustomerID, cr.AccountID
ORDER BY credited_inr DESC;
