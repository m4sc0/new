import shutil
import os
from pathlib import Path
from image import TemplateImage, get_local_image_path
from template_metadata import TemplateMetadata

def build_template(image: TemplateImage, source_path: Path, force: bool = False, dry_run: bool = False, verbose: bool = False):
    if not source_path.exists() or not source_path.is_dir():
        raise FileNotFoundError(f"Source path does not exist or is not a directory: {source_path}")

    original_metadata_path = source_path / "template.json"
    if not original_metadata_path.exists():
        raise FileNotFoundError(f"Missing 'template.json' in source template folder: {source_path}")

    metadata = TemplateMetadata.load(original_metadata_path)
    metadata.category = image.category
    metadata.name = image.name
    metadata.version = image.version

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
                if file == 'template.json':
                    continue  # will be saved manually later
                src = Path(root) / file
                dst = target_dir / file
                if verbose:
                    print(f"Copy: {src} -> {dst}")
                shutil.copy2(src, dst)

        # save the modified metadata
        metadata.save(target_path / "template.json")

    print(f"Template image '{image}' built successfully")

