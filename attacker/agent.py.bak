# agent.py
# Lightweight, payload-agnostic attacker agent for lab use only.
import json
import importlib
import os
import time
import math
import random
import requests
import csv

MODULES_DIR = "modules"
PAYLOADS_FILE = "payloads.json"
LOG_CSV = "attack_log.csv"
SLEEP_BETWEEN = 1.0
MAX_ITERATIONS = 0   # 0 to run forever, set >0 to limit
QUIET = True        # set True to suppress per-iteration prints

def load_payloads():
    with open(PAYLOADS_FILE, "r") as f:
        return json.load(f)["modules"]

def discover_modules():
    mods = {}
    for fname in os.listdir(MODULES_DIR):
        if not fname.endswith(".py") or fname == "__init__.py":
            continue
        modname = fname[:-3]
        try:
            mod = importlib.import_module(f"modules.{modname}")
        except Exception as e:
            print(f"Failed to import module '{modname}': {e}")
            continue
        if hasattr(mod, "MODULE") and isinstance(mod.MODULE, dict) and "name" in mod.MODULE:
            mods[mod.MODULE["name"]] = mod
        else:
            print(f"Skipping module '{modname}': missing MODULE dict or name key")
    return mods

class UCB1:
    def __init__(self, n_arms):
        self.counts = [0]*n_arms
        self.values = [0.0]*n_arms
        self.total = 0

    def select(self):
        for i in range(len(self.counts)):
            if self.counts[i] == 0:
                return i
        ucb_values = [
            self.values[i] + math.sqrt(2*math.log(self.total) / self.counts[i])
            for i in range(len(self.counts))
        ]
        return int(max(range(len(ucb_values)), key=lambda i: ucb_values[i]))

    def update(self, chosen, reward):
        self.counts[chosen] += 1
        self.total += 1
        n = self.counts[chosen]
        value = self.values[chosen]
        self.values[chosen] = ((n-1)/n)*value + (1/n)*reward

def measure_reward(resp, baseline_text=None):
    """
    Improved reward function:
      - strong reward for server errors (5xx)
      - marker string matches
      - scaled response length delta for novelty
      - small jitter to keep exploration alive
    """
    reward = 0.0
    if resp is None:
        return reward

    status = resp.status_code

    # Strong positive signal for server errors (5xx)
    if 500 <= status < 600:
        reward += 5.0

    # Moderate reward for non-200 but non-5xx (e.g., 4xx)
    elif status != 200:
        reward += 1.0

    # Marker strings (useful for mock_target markers)
    markers = ["UNIQUE_ERROR_42", "marker: A", "marker: B", "ERR500_MARKER"]
    for m in markers:
        if m in resp.text:
            reward += 2.0

    # scaled length delta: larger changes matter more
    if baseline_text is not None and isinstance(baseline_text, str):
        delta = abs(len(resp.text) - len(baseline_text))
        reward += min(delta / 150.0, 5.0)
    else:
        reward += len(resp.text) / 500.0

    # small jitter so arms close in value still get explored
    reward += random.uniform(0, 0.05)
    return reward

def write_log(row):
    write_header = not os.path.exists(LOG_CSV)
    with open(LOG_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if write_header:
            w.writeheader()
        w.writerow(row)

def main_loop():
    payloads = load_payloads()
    modules = discover_modules()
    bandits = {}
    baseline_texts = {}

    for modname, variants in payloads.items():
        n = len(variants)
        bandits[modname] = UCB1(n)
        try:
            mod = modules[modname]
            baseline_variant = variants[-1]
            params = mod.build_params(baseline_variant)
            resp = requests.request(mod.MODULE["method"], mod.MODULE["url"], data=params, timeout=8)
            baseline_texts[modname] = resp.text
            if not QUIET:
                print(f"[{modname}] baseline length {len(resp.text)}")
        except Exception as e:
            baseline_texts[modname] = ""
            print(f"[{modname}] baseline failed: {e}")

    iteration = 0
    try:
        while True:
            iteration += 1
            if MAX_ITERATIONS and iteration > MAX_ITERATIONS:
                print(f"Reached MAX_ITERATIONS={MAX_ITERATIONS}, exiting loop")
                raise KeyboardInterrupt
            for modname, variants in payloads.items():
                if modname not in modules:
                    if not QUIET:
                        print(f"Module '{modname}' not loaded; skipping")
                    continue
                mod = modules[modname]
                idx = bandits[modname].select()
                chosen_variant = variants[idx]
                params = mod.build_params(chosen_variant)
                try:
                    resp = requests.request(mod.MODULE["method"], mod.MODULE["url"], data=params, timeout=8)
                    reward = measure_reward(resp, baseline_texts.get(modname))
                    bandits[modname].update(idx, reward)
                    log_row = {
                        "time": time.time(),
                        "iteration": iteration,
                        "module": modname,
                        "variant_index": idx,
                        "params": json.dumps(params),
                        "status": resp.status_code if resp is not None else None,
                        "resp_len": len(resp.text) if resp is not None else 0,
                        "reward": reward,
                        "counts": json.dumps(bandits[modname].counts),
                        "values": json.dumps(bandits[modname].values)
                    }
                    if not QUIET:
                        print(f"[{modname}] iter {iteration} idx {idx} reward {reward:.2f} status {resp.status_code}")
                    write_log(log_row)
                except Exception as e:
                    if not QUIET:
                        print(f"[{modname}] request error: {e}")
                time.sleep(SLEEP_BETWEEN)
            time.sleep(1.0 + random.random())
    except KeyboardInterrupt:
        print("Stopping agent.")
        try:
            print("\n==== Bandit summary (counts & values) ====")
            for modname,b in bandits.items():
                print(modname)
                print("  counts:", b.counts)
                print("  values:", b.values)
        except Exception:
            pass

if __name__ == "__main__":
    main_loop()
