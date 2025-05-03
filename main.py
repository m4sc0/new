from config import config
from renderer import render_template
from image import TemplateImage, load_local_template_image
from pathlib import Path
import os
import argparse
import datetime
import getpass
import platform
import socket
import uuid

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

def create_project(metadata: dict, template_path: Path, project_name: str, output_dir: Path):
    target_path = output_dir / project_name

    template = metadata.get('template', [])
    default_placeholders = get_default_placeholders(project_name, template)

    placeholders = set(metadata.get("placeholders", [])) | set(default_placeholders.keys())
    replacements = {}

    for placeholder in placeholders:
        if placeholder not in default_placeholders:
            replacements[placeholder] = input(f"{placeholder}: ")
        else:
            replacements[placeholder] = default_placeholders[placeholder]

    render_template(template_path, target_path, replacements)
    print(f"Project created at: {target_path}")

    if config.get_open_main_file() and 'open' in metadata:
        editor = os.environ.get("EDITOR")
        if editor:
            file_to_open = target_path / metadata['open']
            print(f"Opening {file_to_open} in $EDITOR...")
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
    list_parser.add_argument('origin', choices=['local','remote'], default='local', const='local', nargs='?')

    # args
    args = parser.parse_args()

    # conditionals for subparsers
    if args.command == 'create':
        try:
            image = TemplateImage.parse(args.image)
        except ValueError as e:
            print(f"{e}")
            return

        output_dir = Path(args.output).resolve() if args.output else Path.cwd()
        project_name = args.project_name

        try:
            metadata, template_path = load_local_template_image(image)
        except Exception as e:
            print(f"Failed to load image {image}: {e}")
            return

        print(f"Using template '{image}' from: {template_path}")
        print(f"Placeholders: {metadata.get('placeholders', [])}")

        try:
            create_project(metadata, template_path, project_name, output_dir)
        except FileExistsError:
            print(f"Project directory '{(output_dir / project_name)}' already exists.")
    elif args.command == 'list':
        if args.origin == "local":
            from image import list_local_images
            images = list_local_images()
            if not images:
                print("No local templates found")
                return
            print("Available local templates:")
            for img in images:
                print(f" - {img}")
        else:
            print("Listing remote templates is not implemented yet")

if __name__ == "__main__":
    main()

