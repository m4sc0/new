import json
import shutil
import os
from pathlib import Path
from image import TemplateImage, get_local_image_path

def build_template(image: TemplateImage, source_path: Path, force: bool = False, dry_run: bool = False, verbose: bool = False):
    if not source_path.exists() or not source_path.is_dir():
        raise FileNotFoundError(f"Source path does not exist or is not a directory: {source_path}")

    template_json = source_path / "template.json"
    if not template_json.exists():
        raise FileNotFoundError(f"Missing 'template.json' in source template folder: {source_path}")

    target_path = get_local_image_path(image)

    if target_path.exists():
        if not force:
            raise FileExistsError(f"Template image '{image}' already exists. Use --force to overwrite.")
        if verbose:
            print(f"Overwriting existing template at: {target_path}")
        if not dry_run:
            shutil.rmtree(target_path)

    if verbose:
        print(f"Building template {image}")
        print(f"From: {source_path}")
        print(f"To:   {target_path}")

    if not dry_run:
        for root, dirs, files in os.walk(source_path):
            rel_root = Path(root).relative_to(source_path)
            target_dir = target_path / rel_root
            target_dir.mkdir(parents=True, exist_ok=True)

            for file in files:
                src = Path(root) / file
                dst = target_dir / file

                # TODO: add .newignore or 'ignore' field to metadata to exclude files properly
                if file == 'template.json':
                    with open(src, "r", encoding="utf-8") as f:
                        metadata = json.load(f)

                    metadata["category"] = image.category
                    metadata["name"] = image.name
                    metadata["version"] = image.version

                    with open(dst, "w", encoding="utf-8") as f:
                        json.dump(metadata, f, indent=4)

                    if verbose:
                        print(f"Inject metadata and copy: {src} -> {dst}")
                    continue

                if verbose:
                    print(f"Copy: {src} -> {dst}")

                shutil.copy2(src, dst)

    print(f"Template image '{image}' built successfully")
