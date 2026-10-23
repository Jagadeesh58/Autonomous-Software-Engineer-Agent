"""
main.py - Main entry point for the Autonomous Software Engineer Agent.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)


def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(BASE_DIR, "session.log")

    # If user asks for log
    if len(sys.argv) == 2 and sys.argv[1].lower() in ["--log", "-l", "log"]:
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                print(f.read())
        else:
            print(f"Session log not found at {log_path}")
        return

    # If task arguments provided, run directly
    if len(sys.argv) > 1:
        from agent import run_agent
        task = " ".join(sys.argv[1:])
        print(f"Running task: {task}\n")
        run_agent(task)
        return

    # Otherwise launch interactive CLI
    from cli import main as cli_main
    cli_main()


if __name__ == "__main__":
    main()
