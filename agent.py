"""
agent.py - Core agent loop (ReAct pattern: Reason + Act + Observe + Self-Heal).
"""

import json
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOL_MAP, TOOL_SCHEMAS, do_search

# Load .env variables with override
load_dotenv(override=True)

SYSTEM_PROMPT = """You are an expert software engineer agent.
When given a task, you must:
1. PLAN - break the task into clear steps
2. ACT - use tools to complete each step
3. VERIFY - run the code or verify output to confirm it works
4. REPORT - summarize what you did

Rules:
- Always write clean, working code
- Always run code after writing it to verify it works
- If something fails, analyze the error, fix it, and try again
- Use write_file for creating or overwriting files
- Use append_file for adding content to existing files
- Use read_file to check file contents
- Use list_directory to inspect folders and existing files
- Use execute_code for running Python code directly
- Use run_shell for system/shell commands
- Use do_search to search the web for documentation or solutions
- Use install_package to install any required Python library via pip
- Use git_commit to save completed work
"""


def get_client_and_model():
    """Resolve API key, base URL, and model based on environment variables."""
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    groq_key = os.environ.get("GROQ_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    api_key = openrouter_key or groq_key or openai_key
    if not api_key:
        raise ValueError(
            "Missing API key! Please set OPENROUTER_API_KEY, GROQ_API_KEY, or OPENAI_API_KEY in your .env file."
        )

    custom_base_url = os.environ.get("OPENAI_BASE_URL")
    custom_model = os.environ.get("AGENT_MODEL")

    if openrouter_key:
        base_url = custom_base_url or "https://openrouter.ai/api/v1"
        model = custom_model or "meta-llama/llama-3.1-8b-instruct"
    elif groq_key:
        base_url = custom_base_url or "https://api.groq.com/openai/v1"
        model = custom_model or "llama-3.3-70b-versatile"
    else:
        base_url = custom_base_url
        model = custom_model or "gpt-4o-mini"

    client = OpenAI(api_key=api_key, base_url=base_url)
    return client, model


def log(entry: str):
    """Append a timestamped entry to session.log."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {entry}"
    try:
        with open("session.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def normalize_tool_args(name: str, args: dict) -> dict:
    """Normalize common tool parameter name variations emitted by different models."""
    if not isinstance(args, dict):
        return {}

    normalized = dict(args)

    # File path normalization
    if "path" not in normalized:
        for alias in ("file_name", "filepath", "filename", "file"):
            if alias in normalized:
                normalized["path"] = normalized.pop(alias)
                break

    # Code vs input
    if name == "execute_code":
        if "code" not in normalized and "input" in normalized:
            normalized["code"] = normalized.pop("input")

    # Command vs cmd / input
    if name == "run_shell":
        if "command" not in normalized:
            for alias in ("cmd", "input", "shell_command"):
                if alias in normalized:
                    normalized["command"] = normalized.pop(alias)
                    break

    # Search query
    if name == "do_search":
        if "query" not in normalized:
            for alias in ("search_query", "q", "input"):
                if alias in normalized:
                    normalized["query"] = normalized.pop(alias)
                    break

    # Directory path
    if name == "list_directory":
        if "path" not in normalized:
            for alias in ("dir", "directory", "folder"):
                if alias in normalized:
                    normalized["path"] = normalized.pop(alias)
                    break

    # Package name
    if name == "install_package":
        if "package" not in normalized:
            for alias in ("pkg", "package_name", "name"):
                if alias in normalized:
                    normalized["package"] = normalized.pop(alias)
                    break

    # Git commit message
    if name == "git_commit":
        if "message" not in normalized:
            for alias in ("msg", "commit_message"):
                if alias in normalized:
                    normalized["message"] = normalized.pop(alias)
                    break

    return normalized


def trim_history_for_context(messages: list, max_recent: int = 14) -> list:
    """Keep system & task prompt while truncating old tool outputs to preserve context window."""
    if len(messages) <= max_recent:
        return messages

    # Keep the first user message intact
    managed = [messages[0]]
    # Keep the recent history, but truncate oversized outputs in older entries
    tail = messages[1:]
    for i, msg in enumerate(tail):
        if i < len(tail) - 6 and msg.get("role") == "tool":
            content = msg.get("content", "")
            if len(content) > 1500:
                managed.append({
                    **msg,
                    "content": content[:1500] + "\n... [output truncated for context limit]"
                })
                continue
        managed.append(msg)
    return managed


def run_agent(task: str, max_steps: int = 15, search_first: bool = False):
    """Run the ReAct autonomous agent loop."""
    try:
        client, model = get_client_and_model()
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        log(f"CONFIG ERROR: {str(e)}")
        return

    messages = []

    with open("session.log", "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"NEW SESSION: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"TASK: {task}\n")
        f.write(f"MODEL: {model}\n")
        f.write(f"{'='*50}\n")

    if search_first:
        print("\n🔍 Searching web for context...")
        search_result = do_search(task)
        log(f"WEB SEARCH: {task[:100]}")
        messages.append({
            "role": "user",
            "content": f"Task: {task}\n\nWeb search results for context:\n{search_result}"
        })
    else:
        messages.append({"role": "user", "content": task})

    print(f"\nTask: {task}\n" + "=" * 50)
    log(f"TASK STARTED: {task[:100]}")

    step = 0
    error_count = 0

    while step < max_steps:
        step += 1
        print(f"\n--- Step {step} ---")
        log(f"STEP {step} STARTED")

        managed_messages = trim_history_for_context(messages)

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + managed_messages,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
                max_tokens=2048
            )
        except Exception as e:
            print(f"❌ API Error: {e}")
            log(f"API ERROR: {str(e)}")
            break

        msg = response.choices[0].message
        content = getattr(msg, "content", None)
        if content is None and isinstance(msg, dict):
            content = msg.get("content", "")

        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls is None and isinstance(msg, dict):
            tool_calls = msg.get("tool_calls", [])
        tool_calls = tool_calls or []

        # Format assistant tool calls cleanly for chat history
        formatted_tool_calls = []
        for idx, tc in enumerate(tool_calls):
            if hasattr(tc, "model_dump"):
                tc_dict = tc.model_dump()
            elif isinstance(tc, dict):
                tc_dict = dict(tc)
            else:
                tc_dict = {
                    "id": getattr(tc, "id", f"call_{step}_{idx}"),
                    "type": "function",
                    "function": {
                        "name": getattr(tc.function, "name", "unknown") if hasattr(tc, "function") else "unknown",
                        "arguments": getattr(tc.function, "arguments", "{}") if hasattr(tc, "function") else "{}"
                    }
                }
            if not tc_dict.get("id"):
                tc_dict["id"] = f"call_{step}_{idx}"
            formatted_tool_calls.append(tc_dict)

        assistant_entry = {
            "role": "assistant",
            "content": content or ""
        }
        if formatted_tool_calls:
            assistant_entry["tool_calls"] = formatted_tool_calls

        messages.append(assistant_entry)

        if content:
            print(f"Agent thinking: {content[:200]}")
            log(f"THINKING: {content[:200]}")

        if not formatted_tool_calls:
            print(f"\n✅ DONE!\nAgent: {content}")
            log(f"TASK COMPLETED: {str(content)[:200]}")
            break

        for idx, tool_call in enumerate(formatted_tool_calls):
            tool_call_id = tool_call.get("id", f"call_{step}_{idx}")
            func = tool_call.get("function", {})
            name = func.get("name", "unknown_tool")
            raw_args = func.get("arguments", "{}")

            try:
                args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args or {}
            except json.JSONDecodeError:
                args = {"input": raw_args}

            args = normalize_tool_args(name, args)

            print(f"\n🔧 Tool: {name}")
            print(f"   Input: {str(args)[:150]}")
            log(f"TOOL: {name} | INPUT: {str(args)[:150]}")

            fn = TOOL_MAP.get(name)
            if not fn:
                result = f"Error: Tool '{name}' not found. Available tools: {', '.join(TOOL_MAP.keys())}"
            else:
                try:
                    result = fn(**args)
                except TypeError as e:
                    # Fallback if arguments were wrapped
                    try:
                        result = fn(args)
                    except Exception:
                        result = f"Error calling tool {name}: {e}"
                except Exception as e:
                    result = f"Error executing tool {name}: {str(e)}"

            result_str = str(result)
            print(f"   Result: {result_str[:200]}")
            log(f"RESULT: {result_str[:200]}")

            tool_message = {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": name,
                "content": result_str
            }

            # Self-healing detection
            if any(word in result_str.lower() for word in ["error", "traceback", "exception", "failed"]):
                error_count += 1
                print(f"   ⚠️ Error detected (attempt {error_count}/3)")
                log(f"ERROR DETECTED (attempt {error_count}/3)")

                if error_count >= 3:
                    tool_message["content"] = result_str + "\n\nYou have failed 3 times. Please explain what went wrong and conclude."
                else:
                    tool_message["content"] = result_str + "\n\nThis failed. Please analyze the error and try a different approach."
            else:
                error_count = 0

            messages.append(tool_message)

    if step >= max_steps:
        print("\n⚠️ Max steps reached.")
        log("MAX STEPS REACHED")

    print("\n📋 Session log saved to session.log")
