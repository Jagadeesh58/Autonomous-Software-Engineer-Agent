from dotenv import load_dotenv
load_dotenv()

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich import print as rprint
from agent import run_agent
import sys

console = Console()

def show_banner():
    banner = Text()
    banner.append("🤖 Autonomous Software Engineer Agent\n", style="bold cyan")
    banner.append("Built with Groq + Llama 3.3 70B\n", style="dim")
    banner.append("Type your task and press Enter. Type 'exit' to quit.", style="dim")
    console.print(Panel(banner, border_style="cyan", padding=(1, 2)))

def show_divider():
    console.print(Rule(style="dim"))

def main():
    show_banner()

    while True:
        try:
            console.print("\n[bold green]You:[/bold green] ", end="")
            task = input().strip()

            if not task:
                continue

            if task.lower() in ["exit", "quit", "bye"]:
                console.print(Panel(
                    "[bold cyan]Goodbye! Your agent is ready whenever you need it. 🚀[/bold cyan]",
                    border_style="cyan"
                ))
                sys.exit(0)

            if task.lower() == "log":
                console.print(Panel("[bold]Showing session log...[/bold]", border_style="yellow"))
                try:
                    with open("F:/agent/session.log", "r") as f:
                        content = f.read()
                    console.print(content)
                except:
                    console.print("[red]No session log found yet.[/red]")
                continue

            show_divider()
            console.print(f"\n[bold yellow]🤖 Agent working on:[/bold yellow] {task}\n")

            run_agent(task)

            show_divider()
            console.print("[bold green]✅ Task complete! Give me another task or type 'exit'.[/bold green]")

        except KeyboardInterrupt:
            console.print("\n\n[bold cyan]Stopped. Type 'exit' to quit or give a new task.[/bold cyan]")
            continue

        except Exception as e:
            console.print(f"\n[bold red]Error: {e}[/bold red]")
            continue

if __name__ == "__main__":
    main()