"""
cli.py - Interactive CLI for the Autonomous Software Engineer Agent.
"""

import sys
import os
import argparse
from dotenv import load_dotenv

# Load .env FIRST, override stale env vars
load_dotenv(override=True)

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from agent import run_agent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
console = Console()


def show_banner():
    banner = Text()
    banner.append("Autonomous Software Engineer Agent\n", style="bold cyan")
    banner.append("Built with Groq + Llama 3.3 70B\n", style="dim")
    banner.append("-" * 40 + "\n", style="dim cyan")
    banner.append("Commands:\n", style="bold white")
    banner.append("  Type your task and press Enter\n", style="dim")
    banner.append("  'search <task>' - web search first\n", style="dim")
    banner.append("  'log'           - view session log\n", style="dim")
    banner.append("  'help'          - show this help\n", style="dim")
    banner.append("  'exit'          - quit\n", style="dim")
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
            do_search = args.search
            if task.lower().startswith("search "):
                task = task[7:].strip()
                do_search = True

            console.print(Rule(style="dim cyan"))
            if do_search:
                console.print(f"\n[bold yellow]Agent working (with web search):[/bold yellow] {task}\n")
            else:
                console.print(f"\n[bold yellow]Agent working on:[/bold yellow] {task}\n")

            run_agent(task, max_steps=args.steps, search_first=do_search)

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