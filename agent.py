from dotenv import load_dotenv
load_dotenv()

from groq import Groq
from tools import (run_shell, read_file, write_file,
                   execute_code, do_search,
                   install_package, git_commit, TOOL_SCHEMAS)
import json
import os

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
- If something fails, fix it and try again
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

def run_agent(task: str, max_steps: int = 10, search_first: bool = False):
    messages = []

    if search_first:
        print(f"\n🔍 Searching web for context...")
        search_result = do_search(task)
        print(f"Search result: {search_result[:200]}")
        messages.append({
            "role": "user",
            "content": f"Task: {task}\n\nWeb search results for context:\n{search_result}"
        })
    else:
        messages.append({"role": "user", "content": task})

    print(f"\nTask: {task}\n" + "="*50)
    step = 0

    while step < max_steps:
        step += 1
        print(f"\n--- Step {step} ---")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
            max_tokens=2048
        )

        msg = response.choices[0].message
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": msg.tool_calls or []
        })

        if msg.content:
            print(f"Agent thinking: {msg.content[:200]}")

        if not msg.tool_calls:
            print(f"\n✅ DONE!\nAgent: {msg.content}")
            break

        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            name = tool_call.function.name
            print(f"\n🔧 Tool: {name}")
            print(f"   Input: {str(args)[:150]}")
            fn = TOOL_MAP.get(name)
            result = fn(**args) if fn else "Tool not found"
            print(f"   Result: {str(result)[:200]}")
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    if step >= max_steps:
        print("\n⚠️ Max steps reached.")