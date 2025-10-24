#!/usr/bin/env python3
import time, csv, os, subprocess

THRESHOLD = 5       # change this to the number of 5xx hits you want before stopping
AGENT_CMD = "agent.py"  # process pattern to kill

def count_5xx():
    fn = "attack_log.csv"
    if not os.path.exists(fn):
        return 0
    c = 0
    with open(fn, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            try:
                if int(r.get('status') or 0) >= 500:
                    c += 1
            except:
                pass
    return c

print("Monitor started: will stop agent when", THRESHOLD, "5xx records observed.")
try:
    while True:
        c = count_5xx()
        if c >= THRESHOLD:
            print("Threshold reached (", c, "). Stopping agent...")
            subprocess.run(["pkill", "-f", AGENT_CMD])
            break
        time.sleep(1.0)
except KeyboardInterrupt:
    print("Monitor interrupted by user.")
