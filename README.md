# 🤖 Autonomous Software Engineer Agent

An AI-powered agent that can write code, fix bugs, run scripts, install packages, search the web, and commit to Git — all by itself.

Built with **Groq (Llama 3.3 70B)** + **Python**

---

## ✨ Features

- ✍️ Write Python files and run them
- 🔄 Fix its own bugs automatically (self-healing, up to 3 retries)
- 📦 Install any Python package via pip
- 📖 Read and write files with safety guards
- 📂 List directory contents to explore projects
- 🔍 Search the web for documentation and solutions
- 📌 Commit code to Git
- 🧠 Context window management for long tasks
- 📋 Full session logging to `session.log`

---

## 📁 Project Structure

```
agent/
├── agent.py          # Core agent loop (ReAct pattern)
├── tools.py          # Tool implementations + schemas
├── cli.py            # Interactive CLI with Rich
├── app.py            # Sample Flask app (agent-generated)
├── .env              # API keys (not committed)
├── .gitignore         # Git ignore rules
├── requirements.txt  # Python dependencies
├── session.log       # Auto-generated session log
└── README.md         # This file
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Jagadeesh58/Autonomous-Software-Engineer-Agent.git
cd agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API keys

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_key_here
SERPER_API_KEY=your_serper_key_here
```

- Get a openrouter API KEY from (openrouter.ai)
- Get a Serper API key from [serper.dev](https://serper.dev)

### 5. Run the agent

```bash
python cli.py
```

---

## 💡 Usage

### Interactive Mode

```bash
python cli.py
```

Type tasks like:
- `Create a Flask REST API with CRUD operations for a todo app`
- `Fix the bug in buggy.py`
- `search How to implement JWT authentication in Flask` (web search first)

### Non-Interactive Mode

```bash
python cli.py "Create a calculator app in Python"
```

### CLI Options

| Flag | Description |
|------|-------------|
| `--search` | Enable web search before every task |
| `--steps N` | Set max steps per task (default: 15) |

### In-App Commands

| Command | Description |
|---------|-------------|
| `search <task>` | Search the web first, then execute the task |
| `log` | View the last 50 lines of session log |
| `help` | Show help / commands |
| `exit` | Quit the agent |

---

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| `run_shell` | Run any shell command |
| `read_file` | Read file contents (max 100 KB) |
| `write_file` | Write content to a file |
| `append_file` | Append content to a file |
| `list_directory` | List files and folders |
| `execute_code` | Run Python code directly |
| `do_search` | Search the web via Serper API |
| `install_package` | Install Python packages via pip |
| `git_commit` | Stage and commit all changes |

---

## 🧠 How It Works

The agent follows a **ReAct (Reason + Act)** loop:

```
User Task → LLM Plans → Calls Tools → Reads Results → Plans Next Step → ...→ Done
```

1. **PLAN** — The LLM breaks the task into steps
2. **ACT** — Executes each step using tools
3. **VERIFY** — Runs code to confirm it works
4. **SELF-HEAL** — If something fails, analyzes the error and retries (up to 3 times)
5. **REPORT** — Summarizes what was done

---

## 📄 License

MIT License — feel free to use and modify.
