from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.prompt import Confirm

console = Console()

def info(message: str):
    console.print(f"[bold cyan][INFO][/bold cyan] {message}")

def success(message: str):
    console.print(f"[bold green][SUCCESS][/bold green] {message}")

def warning(message: str):
    console.print(f"[bold yellow][WARNING][/bold yellow] {message}")

def error(message: str):
    console.print(f"[bold red][ERROR][/bold red] {message}")

def rule(title: str = ""):
    console.rule(title)

def title(message: str):
    console.print(Panel(Text(message, justify="center", style="bold magenta")))

def prompt(message: str) -> str:
    return Prompt.ask(f"[bold cyan]?[/bold cyan] {message}")

def confirm(message: str) -> bool:
    return Confirm.ask(f"[bold yellow]?[/bold yellow] {message}")

def print_tree(tree):
    console.print(tree)

def print_raw(text: str):
    console.print(text)

def verbose(message: str):
    console.print(f"[dim]{message}[/dim]")

