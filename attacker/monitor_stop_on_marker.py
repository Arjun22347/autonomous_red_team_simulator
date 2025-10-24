#!/usr/bin/env python3
import time, csv, os, subprocess

THRESHOLD = 3            # stop after seeing this many occurrences of the marker
MARKER = "ERR500_MARKER" # marker to look for in response text (logged in CSV 'reward' rows)
AGENT_CMD = "agent.py"

def count_marker():
    fn = "attack_log.csv"
    if not os.path.exists(fn):
        return 0
    c = 0
    with open(fn, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            if MARKER in (r.get('params','') + r.get('reward','') + r.get('status','') + r.get('params','') + r.get('module','')):
                c += 1
    return c

print(f"Monitor started: will stop agent when {THRESHOLD} occurrences of '{MARKER}' observed.")
try:
    while True:
        c = count_marker()
        if c >= THRESHOLD:
            print("Threshold reached (", c, "). Stopping agent...")
            subprocess.run(["pkill", "-f", AGENT_CMD])
            break
        time.sleep(1.0)
except KeyboardInterrupt:
    print("Monitor interrupted by user.")
