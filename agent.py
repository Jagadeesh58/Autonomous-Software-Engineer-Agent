"""
agent.py - Core agent loop for the Autonomous Software Engineer.
Uses Groq (Llama 3.3 70B) with ReAct pattern.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

# IMPORTANT: override=True ensures fresh .env values replace stale env vars
load_dotenv(override=True)

from groq import Groq
from tools import TOOL_MAP, TOOL_SCHEMAS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "session.log")

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert software engineer agent.
When given a task, you must:
1. PLAN - break the task into clear steps
2. ACT - use tools to complete each step
3. VERIFY - run the code to confirm it works
4. REPORT - summarize what you did

Available tools:
- run_shell: Run any shell command
- read_file: Read a file's contents
- write_file: Write content to a file
- append_file: Append content to a file
- list_directory: List files in a directory
- execute_code: Run Python code directly
- do_search: Search the web for info
- install_package: Install Python packages via pip
- git_commit: Stage and commit all changes

Rules:
- Always write clean, working code
- Always run code after writing to verify it works
- If code fails, read the error and fix it (max 3 retries)
- Use list_directory first to understand project structure
"""

MAX_CONTEXT_MESSAGES = 40  # Prevent token overflow


def log_entry(session_log, entry):
    """Write a timestamped log entry."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {entry}"
    session_log.append(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def serialize_tool_calls(tool_calls):
    """Convert Groq SDK tool_call objects to plain dicts."""
    if not tool_calls:
        return []
    result = []
    for tc in tool_calls:
        result.append({
            "id": tc.id,
            "type": "function",
            "function": {
                "name": tc.function.name,
                "arguments": tc.function.arguments,
            }
        })
    return result


def trim_messages(messages):
    """Keep messages within token budget."""
    if len(messages) <= MAX_CONTEXT_MESSAGES:
        return messages
    # Always keep first message (the task)
    return [messages[0]] + messages[-(MAX_CONTEXT_MESSAGES - 1):]


def run_agent(task, max_steps=15, search_first=False):
    """Main agent loop."""
    session_log = []
    messages = []

    # Log new session
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"NEW SESSION: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"TASK: {task}\n")
        f.write(f"{'='*50}\n")

    # Optional web search before starting
    if search_first:
        from tools import do_search
        print("\n>> Searching web for context...")
        search_result = do_search(task)
        log_entry(session_log, f"WEB SEARCH: {task[:100]}")
        log_entry(session_log, f"SEARCH RESULT: {search_result[:200]}")
        messages.append({
            "role": "user",
            "content": f"Task: {task}\n\nWeb search results:\n{search_result}"
        })
    else:
        messages.append({"role": "user", "content": task})

    print(f"\nTask: {task}")
    print("=" * 50)
    log_entry(session_log, f"TASK: {task[:100]}")

    step = 0
    error_count = 0

    while step < max_steps:
        step += 1
        print(f"\n--- Step {step} ---")
        log_entry(session_log, f"STEP {step}")

        # Trim context if too long
        trimmed = trim_messages(messages)

        # Call LLM
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + trimmed,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
                max_tokens=4096,
            )
        except Exception as e:
            error_str = str(e)
            # Groq sometimes fails to generate valid tool calls — retry without tools
            if "tool_use_failed" in error_str or "400" in error_str:
                print("  >> Tool call failed, retrying without tools...")
                log_entry(session_log, "TOOL_USE_FAILED - retrying without tools")
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + trimmed,
                        max_tokens=4096,
                    )
                except Exception as e2:
                    print(f">> API Error: {e2}")
                    log_entry(session_log, f"API ERROR: {str(e2)}")
                    break
            else:
                print(f">> API Error: {e}")
                log_entry(session_log, f"API ERROR: {error_str}")
                break

        msg = response.choices[0].message

        # Store assistant message with serialized tool_calls
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": serialize_tool_calls(msg.tool_calls),
        })

        # Print agent thinking
        if msg.content:
            print(f"Agent: {msg.content[:300]}")
            log_entry(session_log, f"AGENT: {msg.content[:300]}")

        # No tool calls = agent is done
        if not msg.tool_calls:
            print(f"\n[DONE] {msg.content}")
            log_entry(session_log, f"COMPLETED: {(msg.content or '')[:300]}")
            break

        # Execute each tool call
        for tool_call in msg.tool_calls:
            name = tool_call.function.name

            # Parse arguments
            try:
                args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as e:
                result = f"Error: Bad arguments: {e}"
                print(f"  [{name}] {result}")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
                continue

            print(f"  [{name}] {str(args)[:150]}")
            log_entry(session_log, f"TOOL: {name} | ARGS: {str(args)[:150]}")

            # Run the tool
            fn = TOOL_MAP.get(name)
            if fn:
                result = fn(**args)
            else:
                result = f"Error: Unknown tool '{name}'"

            print(f"  Result: {str(result)[:250]}")
            log_entry(session_log, f"RESULT: {str(result)[:250]}")

            # Self-healing: detect errors
            error_words = ["error", "traceback", "exception", "failed"]
            is_error = any(w in str(result).lower() for w in error_words)

            if is_error:
                error_count += 1
                print(f"  !! Error detected ({error_count}/3)")
                log_entry(session_log, f"ERROR ({error_count}/3)")

                if error_count >= 3:
                    print("  !! Max retries reached")
                    log_entry(session_log, "MAX RETRIES")
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result + "\n\nYou have failed 3 times. Explain what went wrong.",
                    })
                else:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result + "\n\nThis failed. Analyze the error and try differently.",
                    })
            else:
                error_count = 0
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

    if step >= max_steps:
        print("\n!! Max steps reached.")
        log_entry(session_log, "MAX STEPS")

    print(f"\nSession log: {LOG_FILE}")
    return session_log