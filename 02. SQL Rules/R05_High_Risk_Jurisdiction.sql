-- R05_High_Risk_Jurisdiction.sql
-- Purpose : List cross-border transactions with high-risk jurisdictions.
-- Logic   : CountryCode in the bank's high-risk list (placeholder codes XA, XB, XC in this synthetic data).
-- Dialect : SQLite. Thresholds are illustrative for this learning project, not regulatory advice.

SELECT a.CustomerID, t.AccountID, t.TxnID, t.TxnDate, t.Direction, t.CountryCode, ROUND(t.Amount, 0) AS amount_inr
FROM Transactions t JOIN Accounts a ON a.AccountID = t.AccountID
WHERE t.CountryCode IN ('XA', 'XB', 'XC')
ORDER BY t.Amount DESC;
