import subprocess
import os
import requests
import git

def run_shell(command: str) -> str:
    result = subprocess.run(
        command, shell=True,
        capture_output=True, text=True, timeout=30
    )
    output = result.stdout + result.stderr
    return output.strip() or "Command ran with no output"

def read_file(path: str) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(path: str, content: str) -> str:
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"File written successfully: {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def execute_code(code: str) -> str:
    try:
        with open("_temp_exec.py", "w") as f:
            f.write(code)
        result = subprocess.run(
            "python _temp_exec.py",
            shell=True, capture_output=True,
            text=True, timeout=30
        )
        os.remove("_temp_exec.py")
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error executing code: {str(e)}"

def do_search(query: str) -> str:
    try:
        api_key = os.environ.get("SERPER_API_KEY")
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        payload = {"q": query, "num": 5}
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        results = []
        for item in data.get("organic", [])[:5]:
            results.append(f"Title: {item.get('title')}\nSnippet: {item.get('snippet')}\n")
        return "\n".join(results) if results else "No results found"
    except Exception as e:
        return f"Search error: {str(e)}"

def install_package(package: str) -> str:
    try:
        result = subprocess.run(
            f"pip install {package}",
            shell=True, capture_output=True,
            text=True, timeout=60
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error installing package: {str(e)}"

def git_commit(message: str) -> str:
    try:
        repo = git.Repo("F:/agent")
        repo.git.add(A=True)
        repo.index.commit(message)
        return f"Committed successfully: {message}"
    except Exception as e:
        return f"Git error: {str(e)}"

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "run_shell",
            "description": "Run a Windows shell command and return output.",
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
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to read"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file"},
                    "content": {"type": "string", "description": "Content to write"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_code",
            "description": "Execute Python code directly and return output.",
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
            "name": "install_package",
            "description": "Install a Python package using pip.",
            "parameters": {
                "type": "object",
                "properties": {
                    "package": {"type": "string", "description": "Package name to install"}
                },
                "required": ["package"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "git_commit",
            "description": "Commit all current changes to git.",
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