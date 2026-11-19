-- R03_Income_Mismatch.sql
-- Purpose : Find customers whose 2024 credits are far above their declared income.
-- Logic   : Total credits in 2024 > 3x DeclaredAnnualIncome and > ₹5 lakh.
-- Dialect : SQLite. Thresholds are illustrative for this learning project, not regulatory advice.

SELECT c.CustomerID, c.Occupation, c.DeclaredAnnualIncome,
       ROUND(SUM(t.Amount), 0)                                 AS credits_2024_inr,
       ROUND(SUM(t.Amount) / c.DeclaredAnnualIncome, 1)        AS times_declared_income
FROM Customers c
JOIN Accounts a     ON a.CustomerID = c.CustomerID
JOIN Transactions t ON t.AccountID = a.AccountID AND t.Direction = 'Credit'
GROUP BY c.CustomerID, c.Occupation, c.DeclaredAnnualIncome
HAVING SUM(t.Amount) > 3 * c.DeclaredAnnualIncome AND SUM(t.Amount) > 500000
ORDER BY times_declared_income DESC;
