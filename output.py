from typing import List
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.tree import Tree

from image import TemplateImage, get_local_image_path
from template_metadata import TemplateMetadata

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

def bytesize(num, suffix="B"):
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(num) < 1000.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1000.0
    return f"{num:.1f}Y{suffix}"

def print_template_tree(tree: Tree, templates: List[TemplateImage]):
    grouped = {}
    for t in templates:
        grouped.setdefault(t.category, {}).setdefault(t.name, []).append(t)

    for cat, names in sorted(grouped.items()):
        cat_node = tree.add(f"[cyan]{cat}/[/cyan]")
        for name, versions in sorted(names.items()):
            name_node = cat_node.add(f"[white]{name}[/white]")
            for t in sorted(versions, key=lambda t: t.version, reverse=True):
                try:
                    metadata = TemplateMetadata.load(get_local_image_path(t) / "template.json")
                    label = f"[dim]{t.version}[/dim] [grey62]\t{metadata.created or '???'}\t{metadata.hash or '???'}\t{bytesize(metadata.size)}[/grey62]"
                except:
                    label = f"[dim]{t.version}[/dim]"
                name_node.add(label)
    
def print_template_output(templates, origin: str, mode: str):
    color = "green" if origin == "local" else "blue"

    if mode == "tree":
        tree = Tree(f"[bold {color}]{origin.title()} Templates[/bold {color}]")
        print_template_tree(tree, templates)
        print_tree(tree)

    elif mode == "table":
        table = Table(title=f"{origin.title()} Templates")
        table.box = box.SIMPLE
        table.add_column("Category")
        table.add_column("Name")
        table.add_column("Version")
        table.add_column("Hash", justify="left")
        table.add_column("Created", justify="left")
        table.add_column("Size", justify="right")
        for t in templates:
            try:
                metadata = TemplateMetadata.load(get_local_image_path(t) / "template.json")
                created = metadata.created or "-"
                hash_ = metadata.hash or "-"
                size = bytesize(metadata.size)
            except:
                created = hash_ = size = "-"

            table.add_row(
                    t.category, 
                    t.name, 
                    t.version, 
                    hash_,  
                    created, 
                    size
                )
        console.print(table)

    elif mode == "quiet":
        for t in templates:
            print(f"{origin}\t{t.category}/{t.name}:{t.version}\t{t.hash}")
