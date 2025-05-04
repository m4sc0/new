import json
from pathlib import Path
from typing import Tuple, List

class TemplateImage:
    def __init__(self, category: str, name: str, version: str) -> None:
        self.category = category
        self.name = name
        self.version = version

    @classmethod
    def parse(cls, ref:str):
        """
        Parse an image string like 'project/python:3.10'
        """
        if ':' not in ref:
            raise ValueError(f"Invalid image reference: '{ref}' (missing version")
        path, version = ref.split(':', 1)
        parts = path.split('/')
        if len(parts) != 2:
            raise ValueError(f"Invalid image reference: '{ref}' (expected category/name)")
        category, name = parts
        return cls(category, name, version)

    def id(self) -> str:
        return f"{self.category}/{self.name}:{self.version}"

    def __str__(self) -> str:
        return self.id()

def get_local_image_path(image: TemplateImage) -> Path:
    return Path.home() / ".cache" / "new" / "templates" / image.category / image.name / image.version

def load_local_template_image(image: TemplateImage) -> Tuple[dict, Path]:
    """
    Loads metadata and path for a local template image
    """
    path = get_local_image_path(image)
    template_json = path / "template.json"

    if not template_json.exists():
        raise FileNotFoundError(f"No local template image found at {path}")

    with template_json.open("r") as f:
        metadata = json.load(f)

    if "placeholders" not in metadata:
        raise ValueError(f"Invalid template.json in image {image.id()}")

    return metadata, path

def list_local_images() -> List[TemplateImage]:
    root = Path.home() / ".cache" / "new" / "templates"
    found = []

    if not root.exists():
        return found

    for category_dir in root.iterdir():
        if not category_dir.is_dir():
            continue

        for name_dir in category_dir.iterdir():
            if not name_dir.is_dir():
                continue

            for version_dir in name_dir.iterdir():
                if not version_dir.is_dir():
                    continue

                template_json = version_dir / "template.json"
                if template_json.exists():
                    found.append(TemplateImage(
                        category=category_dir.name,
                        name=name_dir.name,
                        version=version_dir.name
                        ))

    return found
