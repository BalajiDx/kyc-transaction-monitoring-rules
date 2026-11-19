-- 00_Create_Tables_And_Load.sql
-- Purpose : create the three tables used by the KYC checks and monitoring rules and load the CSVs.
-- Dialect : SQLite 3.25+. From the repo root:
--             sqlite3 kyc_tm.db < "02. SQL Rules/00_Create_Tables_And_Load.sql"
-- Data    : SYNTHETIC (seed 11), 1 Jan - 31 Dec 2024, amounts in INR.
--           'Planted Scenarios.csv' is NOT loaded here: it is only used to score the rules afterwards.

DROP TABLE IF EXISTS Customers; DROP TABLE IF EXISTS Accounts; DROP TABLE IF EXISTS Transactions;
CREATE TABLE Customers (
    CustomerID TEXT PRIMARY KEY, CustomerType TEXT, Occupation TEXT, DeclaredAnnualIncome INTEGER, State TEXT,
    PEP INTEGER, PANAvailable INTEGER, AadhaarVerified INTEGER, AddressProofOnFile INTEGER,
    OnboardingDate TEXT, RiskRating TEXT, LastKYCReviewDate TEXT, EDDCompleted INTEGER);
CREATE TABLE Accounts (AccountID TEXT PRIMARY KEY, CustomerID TEXT REFERENCES Customers(CustomerID),
                       AccountType TEXT, OpenDate TEXT);
CREATE TABLE Transactions (TxnID TEXT PRIMARY KEY, AccountID TEXT REFERENCES Accounts(AccountID), TxnDate TEXT,
                           Channel TEXT, Direction TEXT, Amount REAL, Counterparty TEXT, CountryCode TEXT);
.mode csv
.import --skip 1 "01. Dataset/Customers.csv"    Customers
.import --skip 1 "01. Dataset/Accounts.csv"     Accounts
.import --skip 1 "01. Dataset/Transactions.csv" Transactions
CREATE INDEX ix_tx_acc_date ON Transactions(AccountID, TxnDate);
