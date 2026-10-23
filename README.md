# 🤖 Autonomous Software Engineer Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/Pattern-ReAct%20Loop-orange.svg?style=flat-square" alt="ReAct Loop">
  <img src="https://img.shields.io/badge/Status-Active%20%26%20Tested-brightgreen.svg?style=flat-square" alt="Tested">
  <img src="https://img.shields.io/badge/PRs-Welcome-blue.svg?style=flat-square" alt="PRs Welcome">
</p>

An autonomous, full-cycle AI software engineer agent capable of planning tasks, writing Python code, diagnosing and self-healing runtime errors, installing packages, querying real-time web documentation, and committing completed changes to Git — without human intervention.

Built using the **ReAct (Reason + Act)** pattern with native multi-provider LLM support (**OpenRouter**, **Groq**, or **OpenAI**).

---

## 🌟 Highlights & Key Capabilities

- 🔁 **Autonomous ReAct Cycle**: Implements cyclic reasoning where every step plans, acts via tools, observes the outcome, and evaluates next steps.
- 🩺 **Self-Healing Error Recovery**: Automatically catches tracebacks, runtime errors, and failed commands, analyzing diagnostics and iterating up to 3 times to fix bugs.
- 🛠️ **9 Integrated Engineering Tools**: Supports shell execution, safe file I/O, directory exploration, isolated subprocess execution, live Google web search, pip package installation, and automated Git staging/commit.
- 🔌 **Provider Agnostic**: Works out of the box with OpenRouter (`meta-llama/llama-3.1-8b-instruct`), Groq (`llama-3.3-70b-versatile`), or standard OpenAI models (`gpt-4o-mini`).
- 🧠 **Context Window Guard**: Automatically manages conversation memory by pruning and truncating older tool outputs to avoid token limit errors on long-running tasks.
- 📊 **Audit Trail**: Every thought, tool call, argument, and execution result is logged to `session.log` with timestamps.
- 💻 **Modern Terminal Interface**: Interactive Rich-based CLI with colored panels, real-time status banners, and session history inspection.

---

## 📁 Repository Structure

```
Autonomous-Software-Engineer-Agent/
├── .github/
│   └── workflows/
│       └── test.yml          # Automated CI workflow (Ubuntu & Windows, Python 3.10-3.12)
├── examples/                 # Agent-generated and verified sample projects
│   ├── README.md             # Overview of example scripts
│   ├── api.py                # FastAPI item service with Pydantic
│   ├── app.py                # Flask REST API with calculation routes
│   ├── buggy.py              # Debugging and self-healing challenge
│   ├── calculator.py         # Arithmetic functions module
│   ├── colors.py             # Colorama terminal styling
│   ├── data.py               # Pandas CSV analysis script
│   ├── data.csv              # Sample dataset for data.py
│   ├── even_numbers.py       # Even numbers generator
│   ├── notes.py              # File-based note manager
│   └── todo.py               # CLI todo application
├── .env.example              # Environment variables template
├── .gitignore                # Comprehensive Git ignore rules
├── LICENSE                   # MIT License
├── README.md                 # Project documentation
├── agent.py                  # Core agent ReAct engine & LLM orchestrator
├── ai_agent_complete_guide.md# Complete theoretical guide & interview preparation
├── cli.py                    # Rich-powered interactive CLI interface
├── main.py                   # Unified CLI & direct script execution entry point
├── requirements.txt          # Python dependencies
├── test_suite.py             # 9 automated unit tests verifying tools & agent logic
└── tools.py                  # 9 tool implementations & JSON schemas for function calling
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Jagadeesh58/Autonomous-Software-Engineer-Agent.git
cd Autonomous-Software-Engineer-Agent
```

### 2. Set up virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the template to create your `.env` file:

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and provide your API key:

```env
# Primary LLM provider (Recommended: OpenRouter)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: Real-time Google web search
SERPER_API_KEY=your_serper_api_key_here
```

| Provider | Supported Models | Sign Up |
|----------|------------------|---------|
| **OpenRouter** (Default) | `meta-llama/llama-3.1-8b-instruct`, Claude, GPT-4 | [openrouter.ai](https://openrouter.ai) |
| **Groq** | `llama-3.3-70b-versatile` | [console.groq.com](https://console.groq.com) |
| **OpenAI** | `gpt-4o-mini`, `gpt-4o` | [platform.openai.com](https://platform.openai.com) |
| **Serper** | Google Organic Search API | [serper.dev](https://serper.dev) |

---

## 💡 How to Run

### Interactive Terminal Mode

Launch the full interactive agent terminal:

```bash
python cli.py
```
*(or via `python main.py`)*

#### Example Prompts:
```text
You: Create a python script that downloads a webpage and extracts all titles using BeautifulSoup, then test it.
You: Fix the bug in examples/buggy.py and verify that the test passes.
You: search How to implement rate limiting with Redis in Python.
You: log
You: exit
```

### Single-Task (Batch) Mode

Execute a specific task directly from your command line:

```bash
python cli.py "Create a script that calculates fibonacci numbers and test it"
```
*(or `python main.py "Create a script that calculates fibonacci numbers and test it"`)*

### Command Line Flags

| Flag | Description |
|------|-------------|
| `--search` | Run a real-time web search for relevant documentation before planning |
| `--steps N` | Maximum number of ReAct loop steps allowed (default: 15) |

---

## 🛠️ The 9 Engineering Tools

The agent interacts with the operating system and project files via 9 tools defined in [`tools.py`](tools.py):

| Tool | Function | Description |
|------|----------|-------------|
| `run_shell` | Shell Execution | Run system shell commands safely with stdout/stderr capture |
| `read_file` | File Inspection | Read file contents (up to 100 KB) with existence checks |
| `write_file` | File Creation | Create or overwrite files, automatically creating directories |
| `append_file` | File Append | Append content to existing files without overwriting |
| `list_directory` | Directory Exploration | List folder entries with file sizes and directory indicators |
| `execute_code` | Code Runner | Execute isolated Python code using the active environment interpreter |
| `do_search` | Real-Time Web Search | Query Google via Serper API for technical documentation and solutions |
| `install_package` | Package Installer | Install required Python packages on the fly using `pip` |
| `git_commit` | Version Control | Stage workspace changes and create a timestamped Git commit |

---

## 🧠 Architecture & ReAct Loop

```
                     ┌───────────────────────┐
                     │   User Instruction    │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │  LLM Reason & Plan    │
                     └───────────┬───────────┘
                                 │ Emits Tool Call
                                 ▼
                     ┌───────────────────────┐
                     │   Execute Tool Action │
                     │ (Shell / Code / Git)  │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
           No ───────┤ Execution Successful? ├─────── Yes
          │          └───────────────────────┘          │
          ▼                                             ▼
┌───────────────────┐                         ┌───────────────────┐
│ Self-Healing Loop │                         │  Next Action or   │
│ (Diagnose & Retry │                         │    Final Report   │
│   up to 3 times)  │                         └───────────────────┘
└─────────┬─────────┘
          │ Feedback Injected
          └───────────────────────────► Back to LLM
```

---

## 🧪 Testing

The repository includes a comprehensive unit test suite in [`test_suite.py`](test_suite.py):

```bash
python -m unittest test_suite.py -v
```

All 9 tests verify:
- Complete alignment between `TOOL_MAP` and OpenAI JSON schema definitions (`TOOL_SCHEMAS`)
- Safe file operations (`read_file`, `write_file`, `append_file`)
- Directory listing and path resolution
- Isolated code execution and error capture
- Tool argument alias normalization (`query` vs `search_query`, `command` vs `cmd`, etc.)
- Context window pruning and history truncation

---

## 📚 In-Depth Guide

For a comprehensive breakdown of agentic patterns, ReAct loops, function calling internals, and AI engineer interview preparation, check out:
- [`ai_agent_complete_guide.md`](ai_agent_complete_guide.md)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Feel free to use, modify, and distribute this software for personal or commercial projects.
