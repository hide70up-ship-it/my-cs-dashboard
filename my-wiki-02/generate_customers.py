import csv
import random
from datetime import datetime, timedelta

random.seed(42)

NUM = 500
tiers = [
    ("베이직", 200),
    ("스탠다드", 200),
    ("프리미엄", 100),
]

# Target overall churn
total_churn = int(NUM * 0.25)

# Specified base tier rates to preserve relative pattern
base_rates = {"베이직": 0.35, "스탠다드": 0.20, "프리미엄": 0.10}

# Compute scaled churn counts per tier so sum == total_churn
expected = {}
for name, count in tiers:
    expected[name] = count * base_rates[name]
scale = total_churn / sum(expected.values())
churn_counts = {name: int(round(expected[name] * scale)) for name, _ in tiers}

# Adjust rounding to match total_churn exactly
diff = total_churn - sum(churn_counts.values())
if diff != 0:
    # adjust the largest tier first
    order = sorted(churn_counts.items(), key=lambda x: -x[1])
    i = 0
    while diff != 0:
        name = order[i % len(order)][0]
        churn_counts[name] += 1 if diff > 0 else -1
        diff = total_churn - sum(churn_counts.values())
        i += 1

# Generate customers
customers = []
start_date = datetime(2018, 1, 1)
end_date = datetime.now()
days_range = (end_date - start_date).days

cid = 1
for tier_name, tier_count in tiers:
    for _ in range(tier_count):
        customer_id = f"C{cid:04d}"
        # random join date between start and today
        join = start_date + timedelta(days=random.randint(0, days_range))
        join_date = join.strftime("%Y-%m-%d")
        customers.append({
            "customer_id": customer_id,
            "age_group": random.choice(["18-24","25-34","35-44","45-54","55+"]),
            "subscription_tier": tier_name,
            "join_date": join_date,
            "join_datetime": join,
            "churn_yn": "N",
        })
        cid += 1

# For each tier, mark the most recent joiners as churners according to churn_counts.
for tier_name, _ in tiers:
    tier_customers = [c for c in customers if c["subscription_tier"] == tier_name]
    # sort by join_datetime descending (most recent first)
    tier_customers.sort(key=lambda x: x["join_datetime"], reverse=True)
    k = churn_counts[tier_name]
    for c in tier_customers[:k]:
        c["churn_yn"] = "Y"

# Write CSV
out_path = "synthetic_customers_500.csv"
with open(out_path, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["customer_id","age_group","subscription_tier","join_date","churn_yn"])
    for c in customers:
        writer.writerow([c["customer_id"], c["age_group"], c["subscription_tier"], c["join_date"], c["churn_yn"]])

print(f"Wrote {len(customers)} rows to {out_path}")
print("Churn counts by tier:")
from collections import Counter
cnt = Counter()
for c in customers:
    if c["churn_yn"] == "Y":
        cnt[c["subscription_tier"]] += 1
print(dict(cnt))
