from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.tree import Tree

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

def print_template_tree(tree: Tree, templates):
    grouped = {}
    for t in templates:
        grouped.setdefault(t.category, {}).setdefault(t.name, []).append(t.version)
    for cat, names in sorted(grouped.items()):
        cat_node = tree.add(f"[cyan]{cat}/[/cyan]")
        for name, versions in sorted(names.items()):
            name_node = cat_node.add(f"[white]{name}[/white]")
            for version in sorted(versions, key=lambda v: v, reverse=True):
                name_node.add(f"[dim]{version}[/dim]")
    
def print_template_output(templates, origin: str, mode: str):
    color = "green" if origin == "local" else "blue"
    if mode == "tree":
        tree = Tree(f"[bold {color}]{origin.title()} Templates[/bold {color}]")
        print_template_tree(tree, templates)
        print_tree(tree)

    elif mode == "table":
        table = Table(title=f"{origin.title()} Templates")
        table.add_column("Category")
        table.add_column("Name")
        table.add_column("Version")
        for t in templates:
            table.add_row(t.category, t.name, t.version)
        console.print(table)

    elif mode == "quiet":
        for t in templates:
            print(f"{origin}\t{t.category}/{t.name}:{t.version}")



























