Autonomous Red-Team Simulator (starter)

SAFETY: Run only in an isolated lab environment. Do NOT target real systems.

Quick start:
1. Edit attacker/payloads.json with lab-only values if you wish.
2. From the project root run:
   docker-compose up --build
3. The attacker container runs agent.py which logs to attacker/attack_log.csv

Files:
- docker-compose.yml : starts DVWA and attacker (attacker shares DVWA network namespace)
- attacker/Dockerfile : Python image that runs agent.py
- attacker/agent.py : bandit-based, payload-agnostic orchestrator
- attacker/modules/example_module.py : example module for DVWA login form
- attacker/payloads.json : safe example payloads (lab-only)
