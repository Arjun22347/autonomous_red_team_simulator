# Simple test to ensure agent code runs safely
from attacker.agent import main as agent_main

def test_agent_runs():
    try:
        agent_main(max_iterations=1, quiet=True)
        print("Smoke test passed.")
    except Exception as e:
        print(f"Smoke test failed: {e}")

if __name__ == "__main__":
    test_agent_runs()
