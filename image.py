from pathlib import Path
from typing import Tuple, List
from template_metadata import TemplateMetadata

class TemplateImage:
    def __init__(self, category: str, name: str, version: str) -> None:
        self.category = category
        self.name = name
        self.version = version

    @classmethod
    def parse(cls, ref: str):
        if ':' not in ref:
            raise ValueError(f"Invalid image reference: '{ref}' (missing version)")
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
    return Path.home() / ".cache" / "new" / "images" / image.category / image.name / image.version

def load_local_template_image(image: TemplateImage) -> Tuple[TemplateMetadata, Path]:
    path = get_local_image_path(image)
    metadata_path = path / "template.json"
    if not metadata_path.exists():
        raise FileNotFoundError(f"No local template image found at {path}")
    metadata = TemplateMetadata.load(metadata_path)
    return metadata, path

def list_local_images() -> List[TemplateImage]:
    root = Path.home() / ".cache" / "new" / "images"
    found = []
    if not root.exists():
        return found
    for category_dir in root.iterdir():
        for name_dir in category_dir.iterdir():
            for version_dir in name_dir.iterdir():
                metadata_path = version_dir / "template.json"
                if metadata_path.exists():
                    found.append(TemplateImage(
                        category=category_dir.name,
                        name=name_dir.name,
                        version=version_dir.name
                    ))
    return found

