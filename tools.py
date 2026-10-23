"""
tools.py - All tool functions and schemas for the Autonomous Agent.
"""

import os
import subprocess
import sys
import requests

# Dynamic base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ═══════════════════════════════════════════
#  TOOL FUNCTIONS
# ═══════════════════════════════════════════

def run_shell(command: str) -> str:
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            errors="replace"
        )
        output = (result.stdout + result.stderr).strip()
        return output if output else "Command ran with no output"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error: {str(e)}"


def read_file(path: str) -> str:
    """Read file contents (max 100KB)."""
    try:
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            return f"Error: File not found: {path}"
        if not os.path.isfile(abs_path):
            return f"Error: Path is not a file: {path}"
        size = os.path.getsize(abs_path)
        if size > 100 * 1024:
            return f"Error: File too large ({size:,} bytes). Max is 100KB."
        with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(path: str, content: str) -> str:
    """Write content to a file (creates parent dirs if needed)."""
    try:
        abs_path = os.path.abspath(path)
        parent_dir = os.path.dirname(abs_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(str(content))
        return f"File written: {abs_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def append_file(path: str, content: str) -> str:
    """Append content to end of a file."""
    try:
        abs_path = os.path.abspath(path)
        parent_dir = os.path.dirname(abs_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(abs_path, "a", encoding="utf-8") as f:
            f.write(str(content))
        return f"Content appended to: {abs_path}"
    except Exception as e:
        return f"Error appending: {str(e)}"


def list_directory(path: str = ".") -> str:
    """List files and folders in a directory."""
    try:
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            return f"Error: Directory not found: {path}"
        if not os.path.isdir(abs_path):
            return f"Error: Path is not a directory: {path}"
        entries = sorted(os.listdir(abs_path))
        if not entries:
            return f"Directory is empty: {abs_path}"
        lines = []
        for entry in entries:
            full = os.path.join(abs_path, entry)
            if os.path.isdir(full):
                lines.append(f"  [DIR]  {entry}/")
            else:
                try:
                    size = os.path.getsize(full)
                    lines.append(f"  [FILE] {entry}  ({size:,} bytes)")
                except OSError:
                    lines.append(f"  [FILE] {entry}")
        return f"Contents of {abs_path}:\n" + "\n".join(lines)
    except Exception as e:
        return f"Error listing directory: {str(e)}"


def execute_code(code: str) -> str:
    """Execute Python code in a temp file."""
    temp_file = os.path.join(BASE_DIR, "_temp_exec.py")
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(str(code))
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            errors="replace"
        )
        output = (result.stdout + result.stderr).strip()
        return output if output else "Code executed with no output"
    except subprocess.TimeoutExpired:
        return "Error: Code timed out after 30 seconds"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass


def do_search(query: str) -> str:
    """Search the web using Serper API."""
    try:
        api_key = os.environ.get("SERPER_API_KEY")
        if not api_key:
            return "Error: SERPER_API_KEY not set in environment or .env file"
        resp = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": query, "num": 5},
            timeout=10
        )
        data = resp.json()
        results = []
        for item in data.get("organic", [])[:5]:
            results.append(
                f"Title: {item.get('title')}\n"
                f"Snippet: {item.get('snippet')}\n"
                f"URL: {item.get('link')}\n"
            )
        return "\n".join(results) if results else "No results found"
    except Exception as e:
        return f"Search error: {str(e)}"


def install_package(package: str) -> str:
    """Install a Python package via pip."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True,
            text=True,
            timeout=120,
            encoding="utf-8",
            errors="replace"
        )
        output = (result.stdout + result.stderr).strip()
        return output if output else f"Installed: {package}"
    except Exception as e:
        return f"Error installing: {str(e)}"


def git_commit(message: str) -> str:
    """Stage all changes and commit."""
    try:
        subprocess.run(
            ["git", "add", "-A"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        result = subprocess.run(
            ["git", "commit", "-m", str(message)],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        output = (result.stdout + result.stderr).strip()
        return output if output else f"Committed: {message}"
    except Exception as e:
        return f"Git error: {str(e)}"


# ═══════════════════════════════════════════
#  TOOL MAP — function name -> function
# ═══════════════════════════════════════════

TOOL_MAP = {
    "run_shell": run_shell,
    "read_file": read_file,
    "write_file": write_file,
    "append_file": append_file,
    "list_directory": list_directory,
    "execute_code": execute_code,
    "do_search": do_search,
    "install_package": install_package,
    "git_commit": git_commit,
}


# ═══════════════════════════════════════════
#  TOOL SCHEMAS — sent to LLM for function calling
# ═══════════════════════════════════════════

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "run_shell",
            "description": "Run a shell command and return output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to run"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read file contents (max 100KB).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file. Creates directories if needed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Content to write"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "append_file",
            "description": "Append content to end of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Content to append"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List all files and folders in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path (default: current dir)"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_code",
            "description": "Execute Python code and return output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to execute"}
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "do_search",
            "description": "Search the web for information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "install_package",
            "description": "Install a Python package using pip.",
            "parameters": {
                "type": "object",
                "properties": {
                    "package": {"type": "string", "description": "Package name"}
                },
                "required": ["package"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "git_commit",
            "description": "Stage all changes and commit to git.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Commit message"}
                },
                "required": ["message"]
            }
        }
    }
]
