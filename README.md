# 🤖 Autonomous Software Engineer Agent

An autonomous AI software engineer agent that can write code, fix bugs, run scripts, install packages, search the web, and commit to Git — completely on its own.

Built with **Python**, the **ReAct (Reason + Act)** pattern, and flexible LLM providers (**OpenRouter**, **Groq**, or **OpenAI**).

---

## ✨ Features

- ✍️ **Write & Execute Code**: Writes Python scripts and runs them in a sandboxed subprocess.
- 🔄 **Self-Healing Loop**: Automatically detects tracebacks and runtime errors, analyzing and self-correcting up to 3 times.
- 📦 **Automated Package Management**: Installs required Python packages on the fly using `pip`.
- 📖 **Safe File Operations**: Reads, writes, appends, and inspects project files with size and path guards.
- 📂 **Directory Exploration**: Inspects project structures and file listings.
- 🔍 **Real-Time Web Search**: Queries Google via Serper API for documentation and up-to-date solutions.
- 📌 **Git Version Control**: Automatically stages and commits verified code changes.
- 🧠 **Context Management**: Prevents token overflow by pruning and summarizing long execution histories.
- 📋 **Audit Logging**: Every action, tool call, and thought is logged with timestamps in `session.log`.

---

## 📁 Project Structure

```
Autonomous-Software-Engineer-Agent/
├── agent.py          # Core agent ReAct loop & LLM orchestration
├── tools.py          # 9 tool implementations & JSON schemas
├── cli.py            # Rich interactive terminal interface
├── main.py           # Top-level entry point (interactive or batch mode)
├── test_suite.py     # Automated unit tests for tools & agent logic
├── requirements.txt  # Core Python dependencies
├── .env              # API keys & configuration (not committed)
├── .gitignore        # Git ignore rules
├── session.log       # Timestamped session execution audit log
└── README.md         # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Jagadeesh58/Autonomous-Software-Engineer-Agent.git
cd Autonomous-Software-Engineer-Agent
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```env
# Choose your preferred LLM provider (OpenRouter, Groq, or OpenAI):
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: Serper API key for real-time web search capabilities
SERPER_API_KEY=your_serper_key_here

# Optional: Override default model or API endpoint
# AGENT_MODEL=meta-llama/llama-3.1-8b-instruct
# OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

- **OpenRouter** (Default): Get an API key from [openrouter.ai](https://openrouter.ai)
- **Groq** (Alternative): Set `GROQ_API_KEY=your_key` from [console.groq.com](https://console.groq.com)
- **Serper API**: Get a free search key from [serper.dev](https://serper.dev)

---

## 💡 Usage

### Interactive Mode

Launch the Rich-powered interactive terminal:

```bash
python cli.py
```
*or*
```bash
python main.py
```

Try commands and prompts like:
- `Create a Flask REST API with CRUD operations for a todo app and test it`
- `Fix the bug in buggy.py and verify it works`
- `search How to implement rate limiting in Python`
- `log` — View recent entries from `session.log`
- `help` — Show command help
- `exit` — Quit the session

### Non-Interactive (Single Task) Mode

Run a single task directly from the command line:

```bash
python cli.py "Create a calculator app in Python and test all arithmetic functions"
```
*or*
```bash
python main.py "Create a script that calculates fibonacci numbers and verify output"
```

### CLI Flags

| Flag | Description |
|------|-------------|
| `--search` | Perform web search for context before starting the task |
| `--steps N` | Maximum number of ReAct loop iterations (default: 15) |

---

## 🛠️ Available Tools

The agent has access to 9 tools defined in `tools.py`:

| Tool | Function | Description |
|------|----------|-------------|
| `run_shell` | Shell Execution | Run system shell commands and capture stdout/stderr safely |
| `read_file` | File Inspection | Read file contents (up to 100 KB) with path validation |
| `write_file` | File Creation | Create or overwrite files, automatically creating directories |
| `append_file` | File Update | Append text content to existing files |
| `list_directory` | Directory Listing | Explore project directories, subfolders, and file sizes |
| `execute_code` | Code Runner | Execute isolated Python scripts using the active virtual environment |
| `do_search` | Web Search | Query Google via Serper API for documentation and solutions |
| `install_package` | Package Installer | Install external packages into the active environment via pip |
| `git_commit` | Version Control | Stage all workspace changes and create a Git commit |

---

## 🧠 How It Works

The agent implements a cyclic **ReAct (Reason + Act)** pattern:

```
User Prompt
    │
    ▼
┌───────────────────────────────────────────────┐
│ 1. PLAN: Break task into sequential steps     │
│ 2. ACT: Select tool and execute with params   │
│ 3. OBSERVE: Analyze execution results         │
│ 4. SELF-HEAL: On error, diagnose & retry (≤3) │
└───────────────────────────────────────────────┘
    │
    ▼
Task Completed & Summary Reported
```

1. **Plan**: Formulates an execution strategy based on the system prompt instructions.
2. **Act**: The LLM emits structured tool calls (`TOOL_SCHEMAS`) mapped to real Python functions (`TOOL_MAP`).
3. **Verify**: Always executes written code to verify correctness before proceeding.
4. **Self-Heal**: If a tool returns an error or traceback, the feedback is injected into the next prompt, giving the agent up to 3 opportunities to diagnose and rectify the issue.
5. **Report**: Summarizes all actions taken and files modified.

---

## 🧪 Running Tests

Execute the automated test suite:

```bash
python -m unittest test_suite.py
```

All 9 unit tests verify tool schema alignment, file operations, subprocess sandboxing, parameter normalization, and context trimming.

---

## 📄 License

MIT License — free to use and modify for your own projects.
