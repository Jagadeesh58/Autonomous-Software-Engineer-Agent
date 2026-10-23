"""
cli.py - Interactive CLI for the Autonomous Software Engineer Agent.
"""

import argparse
import os
import sys
from dotenv import load_dotenv

# Load .env FIRST, override stale env vars
load_dotenv(override=True)

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from agent import run_agent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
console = Console()


def show_banner():
    """Display interactive banner with current model info."""
    banner = Text()
    banner.append("🤖 Autonomous Software Engineer Agent\n", style="bold cyan")

    if os.environ.get("OPENROUTER_API_KEY"):
        provider = "OpenRouter"
        model = os.environ.get("AGENT_MODEL", "meta-llama/llama-3.1-8b-instruct")
    elif os.environ.get("GROQ_API_KEY"):
        provider = "Groq"
        model = os.environ.get("AGENT_MODEL", "llama-3.3-70b-versatile")
    elif os.environ.get("OPENAI_API_KEY"):
        provider = "OpenAI"
        model = os.environ.get("AGENT_MODEL", "gpt-4o-mini")
    else:
        provider = "Not Configured"
        model = "Please set API key in .env"

    banner.append(f"Provider: {provider} | Model: {model}\n", style="dim")
    banner.append("-" * 48 + "\n", style="dim cyan")
    banner.append("Commands:\n", style="bold white")
    banner.append("  Type your task and press Enter\n", style="dim")
    banner.append("  'search <task>' - run web search first for context\n", style="dim")
    banner.append("  'log'           - view last 50 lines of session log\n", style="dim")
    banner.append("  'help'          - show this banner\n", style="dim")
    banner.append("  'exit' / 'quit' - exit the program\n", style="dim")
    console.print(Panel(banner, border_style="cyan", padding=(1, 2)))


def main():
    parser = argparse.ArgumentParser(description="Autonomous Software Engineer Agent")
    parser.add_argument("--search", action="store_true", help="Web search before every task")
    parser.add_argument("--steps", type=int, default=15, help="Max steps per task (default: 15)")
    parser.add_argument("task", nargs="*", help="Task to run (non-interactive mode)")
    args = parser.parse_args()

    # Non-interactive mode
    if args.task:
        task = " ".join(args.task)
        console.print(f"\n[bold yellow]Running:[/bold yellow] {task}\n")
        run_agent(task, max_steps=args.steps, search_first=args.search)
        return

    # Interactive mode
    show_banner()

    while True:
        try:
            console.print("\n[bold green]You:[/bold green] ", end="")
            task = input().strip()

            if not task:
                continue

            if task.lower() in ["exit", "quit", "bye"]:
                console.print(Panel(
                    "[bold cyan]Goodbye![/bold cyan]",
                    border_style="cyan"
                ))
                sys.exit(0)

            if task.lower() == "help":
                show_banner()
                continue

            if task.lower() == "log":
                log_path = os.path.join(BASE_DIR, "session.log")
                console.print(Panel("[bold]Session Log[/bold]", border_style="yellow"))
                try:
                    with open(log_path, "r", encoding="utf-8") as f:
                        lines = f.read().strip().split("\n")
                    if len(lines) > 50:
                        console.print(f"[dim](last 50 of {len(lines)} lines)[/dim]\n")
                        console.print("\n".join(lines[-50:]))
                    else:
                        console.print("\n".join(lines))
                except FileNotFoundError:
                    console.print("[red]No session log yet.[/red]")
                continue

            # Inline search command
            search_first = args.search
            if task.lower().startswith("search "):
                task = task[7:].strip()
                search_first = True

            console.print(Rule(style="dim cyan"))
            if search_first:
                console.print(f"\n[bold yellow]Agent working (with web search):[/bold yellow] {task}\n")
            else:
                console.print(f"\n[bold yellow]Agent working on:[/bold yellow] {task}\n")

            run_agent(task, max_steps=args.steps, search_first=search_first)

            console.print(Rule(style="dim cyan"))
            console.print("[bold green]Task complete! Give another task or type 'exit'.[/bold green]")

        except KeyboardInterrupt:
            console.print("\n[bold cyan]Stopped. Type 'exit' to quit.[/bold cyan]")
            continue

        except Exception as e:
            console.print(f"\n[bold red]Error: {e}[/bold red]")
            continue


if __name__ == "__main__":
    main()
