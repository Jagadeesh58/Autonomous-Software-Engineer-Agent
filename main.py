from dotenv import load_dotenv
load_dotenv()

# Print the session log located in the project directory
import os
log_path = os.path.join(os.path.dirname(__file__), "session.log")
try:
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(content)
except FileNotFoundError:
    print(f"Session log not found at {log_path}")