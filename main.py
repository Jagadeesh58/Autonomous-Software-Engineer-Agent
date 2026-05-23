from dotenv import load_dotenv
load_dotenv()

# Just print the session log directly
with open("F:/agent/session.log", "r") as f:
    content = f.read()
    print(content)