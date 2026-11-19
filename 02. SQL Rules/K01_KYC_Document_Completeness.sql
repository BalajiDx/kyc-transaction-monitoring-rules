-- K01_KYC_Document_Completeness.sql
-- Purpose : Find customers with incomplete KYC documents.
-- Logic   : Flag if PAN, Aadhaar verification or address proof is missing; count by risk rating.
-- Dialect : SQLite. Thresholds are illustrative for this learning project, not regulatory advice.

SELECT RiskRating,
       COUNT(*)                                                 AS customers,
       SUM(1 - PANAvailable)                                    AS missing_pan,
       SUM(1 - AadhaarVerified)                                 AS aadhaar_not_verified,
       SUM(1 - AddressProofOnFile)                              AS missing_address_proof,
       SUM(CASE WHEN PANAvailable = 0 OR AadhaarVerified = 0 OR AddressProofOnFile = 0 THEN 1 ELSE 0 END) AS incomplete_kyc,
       ROUND(100.0 * SUM(CASE WHEN PANAvailable = 0 OR AadhaarVerified = 0 OR AddressProofOnFile = 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS incomplete_pct
FROM Customers
GROUP BY RiskRating
ORDER BY CASE RiskRating WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END;
