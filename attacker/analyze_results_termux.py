#!/usr/bin/env python3
import csv
import os
from collections import defaultdict
import math

CSV = "attack_log.csv"
if not os.path.exists(CSV):
    # try results folder latest
    if os.path.exists("results"):
        files = sorted(os.listdir("results"))
        if files:
            CSV = os.path.join("results", files[-1])
        else:
            print("No attack_log.csv found and results/ is empty.")
            raise SystemExit(1)
    else:
        print("No attack_log.csv found.")
        raise SystemExit(1)

variant_rewards = defaultdict(list)
total_rows = 0

with open(CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_rows += 1
        try:
            vi = int(row.get('variant_index', 0))
            reward = float(row.get('reward', 0.0))
        except Exception:
            continue
        variant_rewards[vi].append(reward)

if total_rows == 0:
    print("No rows found in", CSV)
    raise SystemExit(0)

print(f"Loaded {total_rows} rows from {CSV}\n")
print("Variant stats (variant_index : count, mean, max)")
items = sorted(variant_rewards.items(), key=lambda x: x[0])
summary = []
for vi, rewards in items:
    count = len(rewards)
    mean = sum(rewards)/count if count else 0.0
    maximum = max(rewards) if count else 0.0
    summary.append((vi, count, mean, maximum))
    print(f"  {vi:>3} : count={count:<5} mean={mean:.4f} max={maximum:.4f}")

# Try to plot in terminal using plotext if available
try:
    import plotext as plt
    xs = [str(v[0]) for v in summary]
    ys = [v[2] for v in summary]
    plt.clear_figure()
    plt.bar(xs, ys)
    plt.title("Mean reward per variant")
    plt.xlabel("variant_index")
    plt.ylabel("mean reward")
    plt.show()
except Exception:
    # Fallback: ASCII bars scaled to terminal width
    print("\nplotext not installed — showing ASCII bars (install via: pip install plotext)\n")
    max_mean = max([v[2] for v in summary]) if summary else 1.0
    scale = 40.0 / max_mean if max_mean > 0 else 1.0
    for vi, count, mean, maximum in summary:
        bar_len = int(math.floor(mean * scale))
        bar = "#" * bar_len
        print(f"{vi:>3} | {bar} {mean:.4f} (n={count})")

print("\nTop 8 rows by reward:")
# show top rows
rows = []
with open(CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            rows.append((float(row.get('reward', 0.0)), row))
        except Exception:
            continue
rows.sort(key=lambda x: x[0], reverse=True)
for r, row in rows[:8]:
    print(f" reward={r:.4f} module={row.get('module','')} variant={row.get('variant_index','')} status={row.get('status','')} params={row.get('params','')}")
