import os
import shutil
from pathlib import Path
from typing import Dict

def apply_replacements(text: str, replacements: Dict[str, str]) -> str:
    for key, value in replacements.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text

def render_template(template_path: Path, target_path: Path, replacements: Dict[str, str]):
    if target_path.exists():
        raise FileExistsError(f"Target folder '{target_path}' already exists.")

    for root, dirs, files in os.walk(template_path):
        rel_path = Path(root).relative_to(template_path)
        rendered_path = target_path / apply_replacements(str(rel_path), replacements)
        rendered_path.mkdir(parents=True, exist_ok=True)

        for file in files:
            if file == "template.json":
                continue

            src_file = Path(root) / file
            dest_file_name = apply_replacements(file, replacements)
            dest_file_path = rendered_path / dest_file_name

            try:
                with open(src_file, "r", encoding="utf-8") as f:
                    content = f.read()
                content = apply_replacements(content, replacements)
                with open(dest_file_path, "w", encoding="utf-8") as f:
                    f.write(content)
            except UnicodeDecodeError:
                shutil.copy2(src_file, dest_file_path)
