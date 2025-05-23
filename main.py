from config import config
import remote
from renderer import render_template
from image import TemplateImage, load_local_template_image
from builder import build_template
from pathlib import Path
import os
import argparse
import datetime
import getpass
import platform
import socket
import uuid
from template_metadata import TemplateMetadata

from rich.tree import Tree
from image import list_local_images
from remote import list_remote_templates
from output import info, success, warning, error, verbose, print_tree, prompt

def list_templates(origin: str):
    if origin in ("local", "all"):
        templates = list_local_images()
        if not templates:
            warning("No local templates found")
        else:
            tree = Tree("[bold green]Local Templates[/bold green]")
            grouped = {}
            for t in templates:
                grouped.setdefault(t.category, {}).setdefault(t.name, []).append(t.version)
            for cat, names in sorted(grouped.items()):
                cat_node = tree.add(f"[cyan]{cat}/[/cyan]")
                for name, versions in sorted(names.items()):
                    name_node = cat_node.add(f"[white]{name}[/white]")
                    for version in sorted(versions, key=lambda v: v, reverse=True):
                        name_node.add(f"[dim]{version}[/dim]")
            print_tree(tree)

    if origin in ("remote", "all"):
        try:
            templates = list_remote_templates(config.get_remote_url())
        except Exception as e:
            error(f"Failed to fetch remote templates: {e}")
            return

        if not templates:
            warning("No remote templates found")
        else:
            tree = Tree("[bold blue]Remote Templates[/bold blue]")
            grouped = {}
            for t in templates:
                grouped.setdefault(t.category, {}).setdefault(t.name, []).append(t.version)
            for cat, names in sorted(grouped.items()):
                cat_node = tree.add(f"[cyan]{cat}/[/cyan]")
                for name, versions in sorted(names.items()):
                    name_node = cat_node.add(f"[white]{name}[/white]")
                    for version in sorted(versions, key=lambda v: v, reverse=True):
                        name_node.add(f"[dim]{version}[/dim]")
            print_tree(tree)

def get_default_placeholders(project_name: str, template_name: str) -> dict:
    now = datetime.datetime.now()
    return {
        "timestamp": now.strftime("%A, %d. %B %Y %I:%M%p"),
        "date": now.strftime("%Y-%m-%d"),
        "year": now.strftime("%Y"),
        "month": now.strftime("%m"),
        "day": now.strftime("%d"),
        "weekday": now.strftime("%A"),
        "time": now.strftime("%I:%M%p"),
        "user": getpass.getuser(),
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "template_name": template_name,
        "project_name": project_name,
        "project_title": project_name.replace("-", " ").replace("_", " ").title(),
        "uuid": str(uuid.uuid4()),
    }

def create_project(metadata: TemplateMetadata, template_path: Path, project_name: str, output_dir: Path):
    target_path = output_dir / project_name
    template = metadata.template()
    default_placeholders = get_default_placeholders(project_name, template)
    placeholders = set(metadata.placeholders) | set(default_placeholders.keys())
    replacements = {}
    for placeholder in placeholders:
        if placeholder not in default_placeholders:
            replacements[placeholder] = prompt(f"{placeholder}")
        else:
            replacements[placeholder] = default_placeholders[placeholder]

    render_template(template_path, target_path, replacements)
    success(f"Project created at: {target_path}")

    if config.get_open_main_file() and metadata.open:
        editor = os.environ.get("EDITOR")
        if editor:
            file_to_open = target_path / metadata.open
            info(f"Opening {file_to_open} in $EDITOR...")
            os.system(f"{editor} {file_to_open}")

def main():
    parser = argparse.ArgumentParser(
        prog='new',
        description='Create new projects or documents from template images',
        epilog='Example: new create project/python:3.10 my-app\\nMore information: https://github.com/m4sc0/new'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # create parser
    create_parser = subparsers.add_parser('create', help='Create a project from a template image')
    create_parser.add_argument('image', help="Template image (e.g. project/python:3.10)")
    create_parser.add_argument('project_name', help="Target directory / project name")
    create_parser.add_argument('-o', '--output', required=False, help="Output directory (default: current)")

    # list parser

    list_parser = subparsers.add_parser('list', help='List local or remote templates')
    list_parser.add_argument('origin', choices=['local','remote','all'], default='local', const='local', nargs='?')

    # build parser

    build_parser = subparsers.add_parser('build', help='Build a local template image from a folder')
    build_parser.add_argument('image', help='Image reference (e.g. project/python:3.10)')
    build_parser.add_argument('source', help='Path to the source folder')
    build_parser.add_argument('-f', '--force', action='store_true', help='Overwrite if template exists already')
    build_parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed output')
    build_parser.add_argument('--dry-run', action='store_true', help='Show what would happen without creating/modifying anything')

    # pull parser

    pull_parser = subparsers.add_parser('pull', help='Pull a template image from remote')
    pull_parser.add_argument('image', help='Template image (e.g. project/python:3.10)')
    pull_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    # push parser
    push_parser = subparsers.add_parser('push')
    push_parser.add_argument('image')
    push_parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    # conditionals for subparsers
    if args.command == 'create':
        try:
            image = TemplateImage.parse(args.image, config.get_allow_missing_version())
        except ValueError as e:
            error(str(e))
            return

        output_dir = Path(args.output).resolve() if args.output else Path.cwd()
        project_name = args.project_name

        try:
            metadata, template_path = load_local_template_image(image)
        except Exception as e:
            error(f"Failed to load image {image}: {e}")
            return
        info(f"Using template '{image}' from: {template_path}")
        info(f"Placeholders: {metadata.placeholders}")
        try:
            create_project(metadata, template_path, project_name, output_dir)
        except FileExistsError:
            error(f"Project directory '{(output_dir / project_name)}' already exists.")

    elif args.command == 'list':
        list_templates(args.origin)

    elif args.command == 'build':
        try:
            image = TemplateImage.parse(args.image, config.get_allow_missing_version())
        except ValueError as e:
            error(str(e))
            return
        source_path = Path(args.source).resolve()
        try:
            build_template(
                image=image,
                source_path=source_path,
                force=args.force,
                dry_run=args.dry_run,
                verbose=args.verbose
            )
        except Exception as e:
            error(f"Failed to build image: {e}")

    elif args.command == 'pull':
        from remote import pull_template
        try:
            image = TemplateImage.parse(args.image, config.get_allow_missing_version())
        except ValueError as e:
            error(str(e))
            return
        remote_url = config.get_remote_url()
        try:
            info(f"Pulling {image} from {remote_url}...")
            pull_template(remote_url, image, verbose=args.verbose)
            success("Done.")
        except Exception as e:
            error(f"Failed to pull image: {e}")

    elif args.command == 'push':
        from remote import upload_template
        try:
            image = TemplateImage.parse(args.image, config.get_allow_missing_version())
        except ValueError as e:
            error(str(e))
            return
        remote_url = config.get_remote_url()
        try:
            upload_template(remote_url, image, verbose=args.verbose)
        except Exception as e:
            error(f"Upload failed: {e}")

if __name__ == "__main__":
    main()

