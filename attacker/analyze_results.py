#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

CSV = "attack_log.csv"
if not os.path.exists(CSV):
    # try results folder latest
    res = sorted(os.listdir("results")) if os.path.exists("results") else []
    if not res:
        print("No attack_log.csv found and no results/ files present.")
        sys.exit(1)
    CSV = os.path.join("results", res[-1])

df = pd.read_csv(CSV)
# mapping for readability (if payloads.json exists)
try:
    payloads = pd.read_json("payloads.json")["modules"].to_dict()
except Exception:
    payloads = {}

print("\n=== Per-variant stats ===")
stats = df.groupby('variant_index')['reward'].agg(['count','mean','max']).reset_index()
print(stats.to_string(index=False))

# map variant -> example payload (if available)
if payloads:
    print("\nVariant -> example payload:")
    for midx, row in stats.iterrows():
        vi = int(row['variant_index'])
        # print first module's mapping (assumes single module)
        for m, variants in payloads.items():
            if vi < len(variants):
                print(f" variant {vi} -> {variants[vi]}")
                break

# plot mean reward per variant
plt.figure(figsize=(6,3))
plt.bar(stats['variant_index'].astype(str), stats['mean'])
plt.xlabel('variant_index')
plt.ylabel('mean reward')
plt.title('Mean reward per variant')
plt.tight_layout()
out = "results/mean_reward_by_variant.png" if os.path.exists("results") else "mean_reward_by_variant.png"
plt.savefig(out)
print(f"\nSaved chart to {out}")
