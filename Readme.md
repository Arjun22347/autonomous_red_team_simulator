
# Autonomous Red‑Team Simulator (Lab‑only)

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Language](https://img.shields.io/badge/Python-3.11-blue.svg)
![Status](https://img.shields.io/badge/Status-Research%20%26%20Lab%20Tool-yellow)

> **Important:** This project is strictly **lab-only**. It is intended for education, defensive research, and experimentation against systems you own or explicitly have authorization to test. **Do not** use this tool against third‑party or production systems. See **Safety & Responsible Use** below.

---

## What is this?

A compact, modular toolkit that simulates an *adaptive* red‑team attacker in a controlled environment. The simulator demonstrates how a learning attacker (multi‑armed bandit / simple RL-style heuristics) can explore inputs, observe responses, and preferentially repeat inputs that produce interesting signals (errors, markers, or unusual content). It is **intended for defenders and researchers** who want a safe, repeatable playground to develop telemetry, detection, and incident response rules.

**Notable components**
- `attacker/agent.py` — the adaptive agent (UCB bandit) that chooses payload variants, scores responses, and logs results.
- `attacker/mock_target.py` — a small Flask mock web target that emits benign and “interesting” responses (normal pages, marker strings, simulated 5xx errors).
- `attacker/modules/*.py` — endpoint descriptors (module per endpoint) and `payloads.json` with payload variants.
- `analyze_results_termux.py` — lightweight analyzer for Termux / low‑resource environments.
- CI smoke test (`smoke_test.py`) — runs in CI with mocked network interactions (safe for public forks).

---

## Quickstart (safe, 2 terminals)

> These instructions assume you run this in an isolated environment (local VM, lab VM, or air‑gapped device).

1. Start the mock target (Terminal A)
   ```bash
   cd ~/autonomous_red_team_simulator/attacker
   python mock_target.py

The mock target will listen on 0.0.0.0:5000 by default.

2. Start the agent (Terminal B)

cd ~/autonomous_red_team_simulator/attacker
# optionally limit runtime / quiet output
sed -i "s/MAX_ITERATIONS = 300/MAX_ITERATIONS = 120/" agent.py
sed -i "s/QUIET = False/QUIET = True/" agent.py
python agent.py


3. Tail the log in either terminal:

tail -f attack_log.csv


4. Analyze results when finished:

./analyze_results_termux.py




---

Running in Docker (optional)

A Dockerfile is included for convenience. Running containers that perform network interactions must only be done inside isolated lab networks.

Build & run (example):

# from project root
docker build -t art-sim -f attacker/Dockerfile attacker/
# run with network isolation (example)
docker run --network none --rm art-sim

Do not expose containers to public networks.


---

Files & Layout

/
├─ attacker/
│  ├─ agent.py                # adaptive bandit agent
│  ├─ mock_target.py          # Flask mock target (lab-only)
│  ├─ payloads.json           # payload variants (safe defaults)
│  ├─ modules/                # endpoint modules (example_module.py, search_module.py ...)
│  └─ analyze_results_termux.py
├─ smoke_test.py              # safe CI smoke tests (mocks requests)
├─ requirements.txt
├─ LICENSE
├─ README.md
└─ .github/workflows/ci.yml


---

Safety & Responsible Use (READ THIS)

This project contains code that resembles attacker behavior. You must follow these rules:

Run only in isolated, controlled environments (local VM, lab VPC, private network). Do not run connected to the public internet or against systems you do not own.

Do not add or use real exploit payloads in payloads.json unless you have express authorization and a secure test environment.

The agent contains a network isolation guard (best‑effort) that refuses to run if module URLs appear non‑local. Do not bypass it lightly.

If you discover a genuine vulnerability in third‑party software while experimenting, follow responsible disclosure procedures — do not exploit or publish uncoordinated details.



---

How it works (high level)

1. Modules describe endpoints and how to construct requests (MODULE dict + build_params()).


2. Payloads (in payloads.json) are variants that the agent will try.


3. The agent uses a UCB1 (multi‑armed bandit) policy to select which variant to try next, balancing exploration and exploitation.


4. The agent scores responses using a heuristic measure_reward() (status codes, content length deltas, presence of marker strings).


5. All attempts are logged to attack_log.csv for offline analysis.



The learning algorithm is intentionally simple and transparent so defenders can reason about signals and detection.


---

Extending the project

Add a new module: create attacker/modules/<name>_module.py exposing a MODULE dict and build_params(payload_variant).

Add more payload variants in attacker/payloads.json.

Replace the bandit with a simulated RL agent (only in lab) — use the smoke_test.py pattern to validate behavior without network.

Integrate telemetry: run Zeek/Suricata on an isolated test network and correlate agent actions with IDS events.



---

Analysis & visualization

Use analyze_results_termux.py for a Termux- or low-resource analysis (no pandas required).

For richer analysis, copy attack_log.csv to your desktop and analyze with pandas / matplotlib or load into a small notebook.



---

Tests & CI

The repo includes a GitHub Actions workflow (.github/workflows/ci.yml) that:

installs dependencies,

runs a lint step,

executes smoke_test.py which mocks requests.request to avoid network access.


smoke_test.py is a safety‑first test and does not perform network communication.


---

License

This project is published under the Apache License 2.0. See LICENSE for details.


---

Contributing

Contributions are welcome but must follow the CONTRIBUTING.md rules:

include tests for new behavior,

document safety implications,

sign the contributor agreement (if applicable),

follow the CODE_OF_CONDUCT.md.



---

Responsible disclosure

If you find a security issue in this project, please follow SECURITY.md and contact the maintainers.


---

Contact / Maintainer

Project maintained by: Arjun22347 (GitHub). Create issues or pull requests in the repository.


---

Quick FAQ

Q: Can I run this against DVWA or WebGoat?
A: Yes — but only within an isolated VM / private lab network. Ensure the agent’s modules point to localhost or an isolated IP and you have permission.

Q: Can the agent find real vulnerabilities?
A: The agent is a learning toy. It can help surface interesting behavior (5xx errors, marker strings) but it is not a substitute for professional security testing. Use it to augment controlled experiments.


---

Acknowledgements
Built for education and defensive research. Use it responsibly and safely.
