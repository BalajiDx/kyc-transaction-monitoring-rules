-- K02_Periodic_KYC_Review_Overdue.sql
-- Purpose : Which customers are overdue for periodic KYC re-verification on 31 Dec 2024?
-- Logic   : Review cycle by risk: High every 2 years, Medium every 8 years, Low every 10 years (cycle used for this exercise).
-- Dialect : SQLite. Thresholds are illustrative for this learning project, not regulatory advice.

WITH due AS (
    SELECT CustomerID, RiskRating, LastKYCReviewDate,
           date(LastKYCReviewDate, '+' || CASE RiskRating WHEN 'High' THEN 2 WHEN 'Medium' THEN 8 ELSE 10 END || ' years') AS next_review_due
    FROM Customers
)
SELECT RiskRating,
       COUNT(*)                                                             AS customers,
       SUM(CASE WHEN next_review_due < '2024-12-31' THEN 1 ELSE 0 END)      AS overdue,
       ROUND(100.0 * SUM(CASE WHEN next_review_due < '2024-12-31' THEN 1 ELSE 0 END) / COUNT(*), 1) AS overdue_pct,
       MIN(CASE WHEN next_review_due < '2024-12-31' THEN next_review_due END) AS oldest_due_date
FROM due
GROUP BY RiskRating
ORDER BY CASE RiskRating WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END;
