"""
Generate the SYNTHETIC dataset for the KYC & Transaction Monitoring Rules project.

Everything is random (seed 11). No real customer, bank or transaction data is used.
A small number of suspicious patterns ("typologies") are planted on purpose so the rules
can be tested; the list of planted cases is written to Planted Scenarios.csv and is used
ONLY to measure how well the rules work. It is not an input to the rules.

Run:  python generate_dataset.py
Output: Customers.csv, Accounts.csv, Transactions.csv, Planted Scenarios.csv  (this folder)
Period: 1 Jan 2024 - 31 Dec 2024. Amounts in INR.
"""
import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)
HERE = os.path.dirname(os.path.abspath(__file__))
START, END = pd.Timestamp("2024-01-01"), pd.Timestamp("2024-12-31")
N = 1800

occupations = {"Salaried": (420_000, 0.45), "Self-Employed": (600_000, 0.18), "Business Owner": (1_200_000, 0.14),
               "Student": (60_000, 0.08), "Retired": (300_000, 0.08), "Homemaker": (90_000, 0.07)}
occ = rng.choice(list(occupations), N, p=[v[1] for v in occupations.values()])
income = np.array([max(30_000, rng.lognormal(np.log(occupations[o][0]), 0.45)) for o in occ]).round(-3)
cust = pd.DataFrame({
    "CustomerID": [f"K{i:05d}" for i in range(1, N + 1)],
    "CustomerType": np.where(occ == "Business Owner", rng.choice(["Individual", "Sole Proprietor"], N, p=[0.4, 0.6]), "Individual"),
    "Occupation": occ,
    "DeclaredAnnualIncome": income.astype(int),
    "State": rng.choice(["Puducherry", "Tamil Nadu", "Karnataka", "Kerala", "Maharashtra", "Delhi"], N,
                        p=[0.2, 0.38, 0.14, 0.1, 0.1, 0.08]),
    "PEP": (rng.random(N) < 0.01).astype(int),
    "PANAvailable": (rng.random(N) > 0.06).astype(int),
    "AadhaarVerified": (rng.random(N) > 0.04).astype(int),
    "AddressProofOnFile": (rng.random(N) > 0.05).astype(int),
    "OnboardingDate": (pd.Timestamp("2012-01-01") + pd.to_timedelta(rng.integers(0, 365 * 12, N), unit="D")).strftime("%Y-%m-%d"),
})
# customer risk rating: PEPs and some business owners are High
risk = np.where(cust["PEP"] == 1, "High",
                np.where((cust["Occupation"] == "Business Owner") & (rng.random(N) < 0.35), "High",
                         rng.choice(["Low", "Medium"], N, p=[0.72, 0.28])))
cust["RiskRating"] = risk
# last periodic KYC review: some are overdue on purpose
last_rev = pd.to_datetime(cust["OnboardingDate"]) + pd.to_timedelta(rng.integers(0, 365 * 9, N), unit="D")
last_rev = last_rev.where(last_rev <= END, END - pd.to_timedelta(rng.integers(30, 900, N), unit="D"))
cust["LastKYCReviewDate"] = last_rev.dt.strftime("%Y-%m-%d")
cust["EDDCompleted"] = np.where(cust["RiskRating"] == "High", (rng.random(N) > 0.2).astype(int), 0)

acc = pd.DataFrame({
    "AccountID": [f"AC{i:06d}" for i in range(1, N + 1)],
    "CustomerID": cust["CustomerID"],
    "AccountType": np.where(cust["CustomerType"] == "Sole Proprietor", "Current", "Savings"),
    "OpenDate": cust["OnboardingDate"],
})

# ------------------------------------------------------------ normal activity
tx = []
cps = [f"CP{i:05d}" for i in range(1, 2500)]
for i, c in cust.iterrows():
    a = acc.at[i, "AccountID"]
    monthly_in = c["DeclaredAnnualIncome"] / 12
    for m in range(1, 13):
        d0 = pd.Timestamp(2024, m, 1)
        if c["Occupation"] in ("Salaried", "Retired"):
            tx.append([a, d0 + pd.Timedelta(days=int(rng.integers(0, 5))), "NEFT", "Credit",
                       round(monthly_in * rng.uniform(0.95, 1.05), 2), "Employer/Pension", "IN"])
        elif c["Occupation"] in ("Self-Employed", "Business Owner"):
            for _ in range(int(rng.integers(2, 7))):
                tx.append([a, d0 + pd.Timedelta(days=int(rng.integers(0, 28))),
                           rng.choice(["UPI", "NEFT", "Cash Deposit"], p=[0.5, 0.35, 0.15]), "Credit",
                           round(monthly_in / 4 * rng.uniform(0.3, 1.6), 2), rng.choice(cps), "IN"])
        else:
            if rng.random() < 0.7:
                tx.append([a, d0 + pd.Timedelta(days=int(rng.integers(0, 28))), "UPI", "Credit",
                           round(monthly_in * rng.uniform(0.5, 1.5), 2), rng.choice(cps), "IN"])
        for _ in range(int(rng.integers(3, 12))):
            ch = rng.choice(["UPI", "POS", "ATM", "NEFT"], p=[0.55, 0.2, 0.15, 0.1])
            amt = monthly_in * rng.uniform(0.02, 0.18)
            if ch == "ATM":
                amt = min(round(amt, -2) or 500, 40_000)
            tx.append([a, d0 + pd.Timedelta(days=int(rng.integers(0, 28))), ch, "Debit", round(amt, 2),
                       rng.choice(cps) if ch != "ATM" else "ATM", "IN"])

# ------------------------------------------------------- planted typologies
planted = []
pool = list(range(N))
rng.shuffle(pool)


def take(k):
    return [pool.pop() for _ in range(k)]


# 1. Structuring: several cash deposits just under the ₹50,000 PAN-reporting threshold
for i in take(14):
    a, d = acc.at[i, "AccountID"], START + pd.Timedelta(days=int(rng.integers(20, 300)))
    smart = rng.random() < 0.25          # some spread deposits out to stay under the rule's window
    for k in range(int(rng.integers(4, 8))):
        gap = int(k * rng.integers(6, 9)) if smart else int(rng.integers(0, 10))
        tx.append([a, d + pd.Timedelta(days=gap), "Cash Deposit", "Credit",
                   float(rng.integers(45_000, 49_900)), "Branch cash", "IN"])
    planted.append([cust.at[i, "CustomerID"], a, "Structuring", d.strftime("%Y-%m-%d")])
# 2. Pass-through / rapid movement: large inflow moved out within 2 days
for i in take(12):
    a, d = acc.at[i, "AccountID"], START + pd.Timedelta(days=int(rng.integers(10, 330)))
    for k in range(int(rng.integers(2, 5))):
        amt = float(rng.integers(300_000, 1_500_000))
        dd = d + pd.Timedelta(days=int(k * rng.integers(10, 30)))
        tx.append([a, dd, "RTGS", "Credit", amt, rng.choice(cps), "IN"])
        smart = rng.random() < 0.2       # some wait 3-4 days and keep back more than 10%
        out_days = int(rng.integers(3, 5)) if smart else int(rng.integers(0, 2))
        share = rng.uniform(0.80, 0.88) if smart else rng.uniform(0.92, 0.99)
        tx.append([a, dd + pd.Timedelta(days=out_days), "RTGS", "Debit", round(amt * share, 2), rng.choice(cps), "IN"])
    planted.append([cust.at[i, "CustomerID"], a, "Pass-through (rapid in/out)", d.strftime("%Y-%m-%d")])
# 3. Income mismatch: low declared income (students / homemakers) with large credits
cand = [i for i in pool if cust.at[i, "Occupation"] in ("Student", "Homemaker")][:10]
for i in cand:
    pool.remove(i)
    a, d = acc.at[i, "AccountID"], START + pd.Timedelta(days=int(rng.integers(10, 330)))
    for k in range(int(rng.integers(3, 6))):
        tx.append([a, d + pd.Timedelta(days=int(rng.integers(0, 40))), rng.choice(["UPI", "IMPS", "NEFT"]), "Credit",
                   float(rng.integers(120_000, 450_000)), rng.choice(cps), "IN"])
    planted.append([cust.at[i, "CustomerID"], a, "Income mismatch", d.strftime("%Y-%m-%d")])
# 4. Many-to-one funnelling: many different senders pay in small amounts within a week
for i in take(8):
    a, d = acc.at[i, "AccountID"], START + pd.Timedelta(days=int(rng.integers(10, 330)))
    for k in range(int(rng.integers(18, 30))):
        tx.append([a, d + pd.Timedelta(days=int(rng.integers(0, 7))), "UPI", "Credit",
                   float(rng.integers(4_000, 19_000)), f"CPX{rng.integers(1, 99999):05d}", "IN"])
    planted.append([cust.at[i, "CustomerID"], a, "Funnel account (many senders)", d.strftime("%Y-%m-%d")])
# 5. High-risk jurisdiction transfers
for i in take(7):
    a, d = acc.at[i, "AccountID"], START + pd.Timedelta(days=int(rng.integers(10, 330)))
    for k in range(int(rng.integers(1, 4))):
        tx.append([a, d + pd.Timedelta(days=int(rng.integers(0, 60))), "SWIFT", rng.choice(["Debit", "Credit"]),
                   float(rng.integers(200_000, 2_000_000)), rng.choice(cps), rng.choice(["XA", "XB", "XC"])])
    planted.append([cust.at[i, "CustomerID"], a, "High-risk jurisdiction", d.strftime("%Y-%m-%d")])

# --------------------------------- legitimate look-alikes (NOT suspicious)
# These are normal customers whose activity happens to trip a rule; they make the
# false-positive rate realistic and are deliberately not in Planted Scenarios.csv.
# a) small shops paid by many different customers over UPI
shops = [i for i in pool if cust.at[i, "Occupation"] in ("Self-Employed", "Business Owner")][:22]
for i in shops:
    pool.remove(i)
    a = acc.at[i, "AccountID"]
    for w in range(int(rng.integers(2, 6))):
        d = START + pd.Timedelta(days=int(rng.integers(0, 350)))
        for k in range(int(rng.integers(15, 26))):
            tx.append([a, d + pd.Timedelta(days=int(rng.integers(0, 7))), "UPI", "Credit",
                       float(rng.integers(150, 2_500)), f"CPS{rng.integers(1, 99999):05d}", "IN"])
# b) one-off large credit (property sale / FD maturity) used to buy a house a day later
for i in take(16):
    a, d = acc.at[i, "AccountID"], START + pd.Timedelta(days=int(rng.integers(10, 340)))
    amt = float(rng.integers(1_500_000, 6_000_000))
    tx.append([a, d, "NEFT", "Credit", amt, "Property sale / FD maturity", "IN"])
    tx.append([a, d + pd.Timedelta(days=1), "RTGS", "Debit", round(amt * rng.uniform(0.9, 0.98), 2), "Builder / seller", "IN"])
# c) cash-heavy small businesses depositing the day's takings
cashb = [i for i in pool if cust.at[i, "Occupation"] in ("Self-Employed", "Business Owner")][:12]
for i in cashb:
    pool.remove(i)
    a = acc.at[i, "AccountID"]
    for w in range(int(rng.integers(2, 5))):
        d = START + pd.Timedelta(days=int(rng.integers(0, 350)))
        for k in range(3):
            tx.append([a, d + pd.Timedelta(days=int(k * 3)), "Cash Deposit", "Credit",
                       float(rng.integers(40_000, 49_999)), "Branch cash", "IN"])

txdf = pd.DataFrame(tx, columns=["AccountID", "TxnDate", "Channel", "Direction", "Amount", "Counterparty", "CountryCode"])
txdf["TxnDate"] = pd.to_datetime(txdf["TxnDate"]).clip(upper=END).dt.strftime("%Y-%m-%d")
txdf = txdf.sort_values(["TxnDate", "AccountID"]).reset_index(drop=True)
txdf.insert(0, "TxnID", [f"TX{i:07d}" for i in range(1, len(txdf) + 1)])

cust.to_csv(os.path.join(HERE, "Customers.csv"), index=False)
acc.to_csv(os.path.join(HERE, "Accounts.csv"), index=False)
txdf.to_csv(os.path.join(HERE, "Transactions.csv"), index=False)
pd.DataFrame(planted, columns=["CustomerID", "AccountID", "Typology", "FirstDate"]).to_csv(
    os.path.join(HERE, "Planted Scenarios.csv"), index=False)
print(f"customers {len(cust):,}  transactions {len(txdf):,}  planted cases {len(planted)}")
