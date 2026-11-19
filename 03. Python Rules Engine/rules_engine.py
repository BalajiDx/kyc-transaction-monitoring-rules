"""
Transaction-monitoring rules engine (Python / pandas) for the SYNTHETIC KYC & TM learning project.

It runs the same six rules as the SQL scripts in "02. SQL Rules", then:
  1. writes one row per rule hit           -> Output/Rule_Hits.csv
  2. consolidates hits into one alert per customer with a risk score and a priority
                                            -> Output/Alerts.csv
  3. scores the rules against the planted scenarios (which the rules never see)
                                            -> Output/Rule_Evaluation.csv

Run from this folder:  python rules_engine.py
Thresholds are illustrative for learning, not regulatory guidance.
"""
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "01. Dataset")
OUT = os.path.join(HERE, "Output")
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------- settings
RULES = {
    # id: (name, typology, weight)
    "R01": ("Cash deposits just under ₹50,000", "Structuring", 30),
    "R02": ("Large credit moved out within 2 days", "Pass-through (rapid in/out)", 35),
    "R03": ("Credits above 3x declared income", "Income mismatch", 20),
    "R04": ("15+ different senders in 7 days", "Funnel account (many senders)", 30),
    "R05": ("Transfer with high-risk jurisdiction", "High-risk jurisdiction", 40),
    "R06": ("Monthly credits above 5x own normal", "Unusual spike", 15),
}
HIGH_RISK_COUNTRIES = {"XA", "XB", "XC"}
RISK_MULTIPLIER = {"High": 1.5, "Medium": 1.2, "Low": 1.0}
PRIORITY = [(80, "P1 - investigate within 2 days"), (50, "P2 - investigate within 7 days"), (0, "P3 - review and close")]

cust = pd.read_csv(os.path.join(DATA, "Customers.csv"))
acc = pd.read_csv(os.path.join(DATA, "Accounts.csv"))
tx = pd.read_csv(os.path.join(DATA, "Transactions.csv"), parse_dates=["TxnDate"])
tx = tx.merge(acc[["AccountID", "CustomerID"]], on="AccountID")
hits = []


def hit(rule, customer, account, first_date, detail, value):
    hits.append({"RuleID": rule, "Rule": RULES[rule][0], "Typology": RULES[rule][1], "CustomerID": customer,
                 "AccountID": account, "FirstSeen": pd.Timestamp(first_date).strftime("%Y-%m-%d"),
                 "Detail": detail, "ValueINR": round(float(value), 0)})


# R01 structuring: >=3 cash deposits of 40,000-49,999 within any 10-day window
cash = tx[(tx.Channel == "Cash Deposit") & (tx.Direction == "Credit") & tx.Amount.between(40000, 49999)]
for (cid, aid), g in cash.groupby(["CustomerID", "AccountID"]):
    g = g.sort_values("TxnDate")
    best = None
    for d in g.TxnDate:
        w = g[(g.TxnDate >= d) & (g.TxnDate <= d + pd.Timedelta(days=9))]
        if len(w) >= 3 and (best is None or w.Amount.sum() > best[1]):
            best = (d, w.Amount.sum(), len(w))
    if best:
        hit("R01", cid, aid, best[0], f"{best[2]} deposits of ₹40-50k in 10 days", best[1])

# R02 pass-through: credit >= 2 lakh, debit of 90-100% within 2 days
big = tx[(tx.Direction == "Credit") & (tx.Amount >= 200000)]
deb = tx[tx.Direction == "Debit"]
pairs = big.merge(deb, on=["AccountID", "CustomerID"], suffixes=("_c", "_d"))
pairs = pairs[(pairs.TxnDate_d >= pairs.TxnDate_c) & (pairs.TxnDate_d <= pairs.TxnDate_c + pd.Timedelta(days=2))
              & pairs.Amount_d.between(0.9 * pairs.Amount_c, pairs.Amount_c)]
for (cid, aid), g in pairs.groupby(["CustomerID", "AccountID"]):
    g = g.drop_duplicates("TxnID_c")
    hit("R02", cid, aid, g.TxnDate_c.min(), f"{len(g)} credit(s) moved out within 2 days", g.Amount_c.sum())

# R03 income mismatch
cr = tx[tx.Direction == "Credit"].groupby("CustomerID").Amount.sum().rename("Credits").reset_index()
cr = cr.merge(cust[["CustomerID", "DeclaredAnnualIncome"]], on="CustomerID")
for _, r in cr[(cr.Credits > 3 * cr.DeclaredAnnualIncome) & (cr.Credits > 500000)].iterrows():
    first = tx[(tx.CustomerID == r.CustomerID) & (tx.Direction == "Credit")].TxnDate.min()
    hit("R03", r.CustomerID, acc.loc[acc.CustomerID == r.CustomerID, "AccountID"].iloc[0], first,
        f"credits {r.Credits / r.DeclaredAnnualIncome:.1f}x declared income", r.Credits)

# R04 funnel: >=15 distinct senders in any 7-day window
crd = tx[tx.Direction == "Credit"][["CustomerID", "AccountID", "TxnDate", "Counterparty", "Amount"]]
counts = crd.groupby("AccountID").Counterparty.nunique()
for aid in counts[counts >= 15].index:
    g = crd[crd.AccountID == aid].sort_values("TxnDate")
    best = None
    for d in g.TxnDate.unique():
        w = g[(g.TxnDate >= d) & (g.TxnDate <= d + pd.Timedelta(days=6))]
        n = w.Counterparty.nunique()
        if n >= 15 and (best is None or n > best[1]):
            best = (d, n, w.Amount.sum())
    if best:
        hit("R04", g.CustomerID.iloc[0], aid, best[0], f"{best[1]} senders in 7 days", best[2])

# R05 high-risk jurisdiction
for (cid, aid), g in tx[tx.CountryCode.isin(HIGH_RISK_COUNTRIES)].groupby(["CustomerID", "AccountID"]):
    hit("R05", cid, aid, g.TxnDate.min(), f"{len(g)} transfer(s) with {', '.join(sorted(g.CountryCode.unique()))}",
        g.Amount.sum())

# R06 monthly spike vs own history
m = tx[tx.Direction == "Credit"].assign(Month=lambda d: d.TxnDate.dt.to_period("M")) \
    .groupby(["CustomerID", "Month"]).Amount.sum().reset_index()
m["Other"] = (m.groupby("CustomerID").Amount.transform("sum") - m.Amount) / (m.groupby("CustomerID").Amount.transform("count") - 1)
for _, r in m[(m.Amount > 5 * m.Other) & (m.Amount > 300000)].iterrows():
    hit("R06", r.CustomerID, acc.loc[acc.CustomerID == r.CustomerID, "AccountID"].iloc[0], r.Month.start_time,
        f"{r.Month} credits {r.Amount / r.Other:.0f}x the customer's normal month", r.Amount)

hits_df = pd.DataFrame(hits).sort_values(["CustomerID", "RuleID"])
hits_df.to_csv(os.path.join(OUT, "Rule_Hits.csv"), index=False)

# ------------------------------------------------- consolidate into alerts
alerts = hits_df.groupby("CustomerID").agg(
    Rules=("RuleID", lambda s: ", ".join(sorted(set(s)))),
    Typologies=("Typology", lambda s: "; ".join(sorted(set(s)))),
    FirstSeen=("FirstSeen", "min"),
    ValueINR=("ValueINR", "max"),
    BaseScore=("RuleID", lambda s: sum(RULES[r][2] for r in set(s))),
).reset_index().merge(cust[["CustomerID", "Occupation", "RiskRating", "PEP", "DeclaredAnnualIncome"]], on="CustomerID")
alerts["RiskScore"] = (alerts.BaseScore * alerts.RiskRating.map(RISK_MULTIPLIER) + alerts.PEP * 20).clip(upper=100).round(0)
alerts["Priority"] = alerts.RiskScore.apply(lambda s: next(p for t, p in PRIORITY if s >= t))
alerts = alerts.sort_values("RiskScore", ascending=False).reset_index(drop=True)
alerts.insert(0, "AlertID", [f"ALT-{i:04d}" for i in range(1, len(alerts) + 1)])
alerts["Status"] = "Open"
alerts.drop(columns="BaseScore").to_csv(os.path.join(OUT, "Alerts.csv"), index=False)

# ------------------------------------------ evaluation vs planted scenarios
planted_path = os.path.join(DATA, "Planted Scenarios.csv")
if os.path.exists(planted_path):
    planted = pd.read_csv(planted_path)
    rows = []
    for rid, (name, typ, _) in RULES.items():
        flagged = set(hits_df.loc[hits_df.RuleID == rid, "CustomerID"])
        target = set(planted.loc[planted.Typology == typ, "CustomerID"])
        any_planted = set(planted.CustomerID)
        rows.append({"RuleID": rid, "Rule": name, "Target typology": typ, "Customers flagged": len(flagged),
                     "Planted cases": len(target) if target else None,
                     "Planted cases caught": len(flagged & target) if target else None,
                     "Recall %": round(100 * len(flagged & target) / len(target), 1) if target else None,
                     "Flags on any planted case %": round(100 * len(flagged & any_planted) / len(flagged), 1) if flagged else None})
    ev = pd.DataFrame(rows)
    alerted = set(alerts.CustomerID)
    all_p = set(planted.CustomerID)
    ev.loc[len(ev)] = {"RuleID": "ALL", "Rule": "Any alert", "Target typology": "All planted",
                       "Customers flagged": len(alerted), "Planted cases": len(all_p),
                       "Planted cases caught": len(alerted & all_p),
                       "Recall %": round(100 * len(alerted & all_p) / len(all_p), 1),
                       "Flags on any planted case %": round(100 * len(alerted & all_p) / len(alerted), 1)}
    ev.to_csv(os.path.join(OUT, "Rule_Evaluation.csv"), index=False)
    print(ev.to_string(index=False))

print(f"\n{len(hits_df)} rule hits -> {len(alerts)} customer alerts")
print(alerts.Priority.value_counts().sort_index().to_string())
