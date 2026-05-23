from dotenv import load_dotenv
from agent import run_agent

load_dotenv()

if __name__ == "__main__":
    run_agent("Create a file called notes.py with a comment saying this is a notes app, then commit it to git with message 'add notes file'.")