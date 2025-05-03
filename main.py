# custom module imports
from config import config
from renderer import render_template
from template_registry import TemplateRegistry

# other modules
from pathlib import Path
import os
import argparse

def resolve_template(type_: str, template_name: str):
    registry = TemplateRegistry(config.get_template_paths())
    return registry.get_template(type_, template_name)

def create_project(metadata, template_path: Path, project_name: str, output_dir: Path):
    target_path = output_dir / project_name

    replacements = {
        "project_name": project_name
    }

    for placeholder in metadata.get("placeholders", []):
        if placeholder not in replacements:
            # In the future: prompt user or load from defaults
            replacements[placeholder] = project_name

    render_template(template_path, target_path, replacements)
    print(f"Project created at: {target_path}")

    # Optionally open the main file
    if config.get_open_main_file() and 'open' in metadata:
        editor = os.environ.get("EDITOR")
        if editor:
            file_to_open = target_path / metadata['open']
            print(f"Opening {file_to_open} in $EDITOR...")
            os.system(f"{editor} {file_to_open}")

def main():
    parser = argparse.ArgumentParser(
        prog='new',
        description='Create new projects or documents from templates',
        epilog='More: https://github.com/m4sc0/new'
    )

    parser.add_argument('type', help="Template category (e.g. project, doc)")
    parser.add_argument('template', help="Template name (e.g. python)")
    parser.add_argument('project_name', help="Name of the new project/folder")

    parser.add_argument('-o', '--output', required=False, help="Target directory (default: current directory)")

    args = parser.parse_args()

    type_ = args.type
    template = args.template
    project_name = args.project_name
    output_dir = Path(args.output).resolve() if args.output else Path.cwd()

    try:
        metadata, template_path = resolve_template(type_, template)
    except FileNotFoundError as e:
        print(f"{e}")
        return

    print(f"Creating '{metadata['name']}' from: {template_path}")
    print(f"Placeholders: {metadata.get('placeholders', [])}")

    try:
        create_project(metadata, template_path, project_name, output_dir)
    except FileExistsError:
        print(f"Project directory '{(output_dir / project_name)}' already exists.")

if __name__ == "__main__":
    main()

