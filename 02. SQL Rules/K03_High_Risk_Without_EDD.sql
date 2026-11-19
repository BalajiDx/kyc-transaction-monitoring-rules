-- K03_High_Risk_Without_EDD.sql
-- Purpose : List high-risk customers (including PEPs) without completed Enhanced Due Diligence.
-- Logic   : RiskRating = 'High' AND EDDCompleted = 0.
-- Dialect : SQLite. Thresholds are illustrative for this learning project, not regulatory advice.

SELECT c.CustomerID, c.Occupation, c.PEP, c.DeclaredAnnualIncome, c.LastKYCReviewDate,
       COUNT(t.TxnID)                AS txns_2024,
       ROUND(SUM(t.Amount), 0)       AS value_2024_inr
FROM Customers c
JOIN Accounts a          ON a.CustomerID = c.CustomerID
LEFT JOIN Transactions t ON t.AccountID = a.AccountID
WHERE c.RiskRating = 'High' AND c.EDDCompleted = 0
GROUP BY c.CustomerID, c.Occupation, c.PEP, c.DeclaredAnnualIncome, c.LastKYCReviewDate
ORDER BY c.PEP DESC, value_2024_inr DESC;
