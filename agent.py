from dotenv import load_dotenv
load_dotenv()

from groq import Groq
from tools import (run_shell, read_file, write_file,
                   execute_code, do_search,
                   install_package, git_commit, TOOL_SCHEMAS)
import json
import os
from datetime import datetime

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert software engineer agent.
When given a task, you must:
1. PLAN - break the task into clear steps
2. ACT - use tools to complete each step
3. VERIFY - run the code to confirm it works
4. REPORT - summarize what you did

Rules:
- Always write clean, working code
- Always run code after writing it to verify
- If code fails, read the error carefully and fix it
- Try maximum 3 times to fix any error before giving up
- Use write_file for saving code to files
- Use execute_code for running quick Python code
- Use run_shell for system commands
- Use read_file to check file contents
- Use install_package to install any library
- Use git_commit to save completed work
"""

TOOL_MAP = {
    "run_shell": run_shell,
    "read_file": read_file,
    "write_file": write_file,
    "execute_code": execute_code,
    "install_package": install_package,
    "git_commit": git_commit
}

def log(session_log: list, entry: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {entry}"
    session_log.append(line)
    with open("session.log", "a") as f:
        f.write(line + "\n")

def run_agent(task: str, max_steps: int = 15, search_first: bool = False):
    session_log = []
    messages = []

    with open("session.log", "a") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"NEW SESSION: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"TASK: {task}\n")
        f.write(f"{'='*50}\n")

    if search_first:
        print(f"\n🔍 Searching web for context...")
        search_result = do_search(task)
        log(session_log, f"WEB SEARCH: {task[:100]}")
        log(session_log, f"RESULT: {search_result[:200]}")
        messages.append({
            "role": "user",
            "content": f"Task: {task}\n\nWeb search results:\n{search_result}"
        })
    else:
        messages.append({"role": "user", "content": task})

    print(f"\nTask: {task}\n" + "="*50)
    log(session_log, f"TASK STARTED: {task[:100]}")

    step = 0
    error_count = 0

    while step < max_steps:
        step += 1
        print(f"\n--- Step {step} ---")
        log(session_log, f"STEP {step} STARTED")

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
                max_tokens=2048
            )
        except Exception as e:
            print(f"❌ API Error: {e}")
            log(session_log, f"API ERROR: {str(e)}")
            break

        msg = response.choices[0].message
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": msg.tool_calls or []
        })

        if msg.content:
            print(f"Agent thinking: {msg.content[:200]}")
            log(session_log, f"THINKING: {msg.content[:200]}")

        if not msg.tool_calls:
            print(f"\n✅ DONE!\nAgent: {msg.content}")
            log(session_log, f"TASK COMPLETED: {msg.content[:200]}")
            break

        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            name = tool_call.function.name
            print(f"\n🔧 Tool: {name}")
            print(f"   Input: {str(args)[:150]}")
            log(session_log, f"TOOL: {name} | INPUT: {str(args)[:150]}")

            fn = TOOL_MAP.get(name)
            result = fn(**args) if fn else "Tool not found"

            print(f"   Result: {str(result)[:200]}")
            log(session_log, f"RESULT: {str(result)[:200]}")

            # Self healing — detect errors and increment counter
            if any(word in str(result).lower() for word in ["error", "traceback", "exception", "failed"]):
                error_count += 1
                print(f"   ⚠️ Error detected (attempt {error_count}/3)")
                log(session_log, f"ERROR DETECTED (attempt {error_count}/3)")

                if error_count >= 3:
                    print("\n❌ Max retries reached. Asking agent to report what went wrong.")
                    log(session_log, "MAX RETRIES REACHED")
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result + "\n\nYou have failed 3 times. Please explain what went wrong and what you tried."
                    })
                    continue
                else:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result + "\n\nThis failed. Please analyze the error carefully and try a different approach."
                    })
            else:
                error_count = 0
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

    if step >= max_steps:
        print("\n⚠️ Max steps reached.")
        log(session_log, "MAX STEPS REACHED")

    print(f"\n📋 Session log saved to session.log")