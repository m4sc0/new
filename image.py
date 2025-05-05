import hashlib
from pathlib import Path
from typing import Tuple, List
from template_metadata import TemplateMetadata
from packaging.version import Version, InvalidVersion

def safe_version(v: str):
    try:
        return Version(v)
    except InvalidVersion:
        return Version("0.0.0")

def compute_template_hash(template_path: Path) -> str:
    hash_obj = hashlib.sha256()

    for file in sorted(template_path.rglob("*")):
        if file.name == "template.json" or not file.is_file():
            continue

        rel_path = file.relative_to(template_path).as_posix()
        hash_obj.update(rel_path.encode("utf-8"))

        with file.open("rb") as f:
            while chunk := f.read(8192):
                hash_obj.update(chunk)

    return hash_obj.hexdigest()[:32]

class TemplateImage:
    def __init__(self, category: str, name: str, version: str) -> None:
        self.category = category
        self.name = name
        self.version = version

    @classmethod
    def parse(cls, ref: str, allow_missing_version: bool = False):
        if ':' in ref:
            path, version = ref.split(':', 1)
            parts = path.split('/')
            if len(parts) != 2:
                raise ValueError(f"Invalid image reference: '{ref}' (expected category/name)")
            category, name = parts
            return cls(category, name, version)
        
        if not allow_missing_version:
            raise ValueError(f"Invalid image reference: '{ref}' (missing version)")

        # Infer latest version
        parts = ref.split('/')
        if len(parts) != 2:
            raise ValueError(f"Invalid image reference: '{ref}' (expected category/name)")
        category, name = parts

        root = Path.home() / ".cache" / "new" / "templates" / category / name
        if not root.exists():
            raise FileNotFoundError(f"No template found for: {ref}")

        versions = sorted([p.name for p in root.iterdir() if p.is_dir()], key=safe_version)
        if not versions:
            raise FileNotFoundError(f"No versions found for: {ref}")

        print(versions)
        latest_version = versions[-1]
        return cls(category, name, latest_version)

    def id(self) -> str:
        return f"{self.category}/{self.name}:{self.version}"

    def __str__(self) -> str:
        return self.id()

def get_local_image_path(image: TemplateImage) -> Path:
    return Path.home() / ".cache" / "new" / "templates" / image.category / image.name / image.version

def load_local_template_image(image: TemplateImage) -> Tuple[TemplateMetadata, Path]:
    path = get_local_image_path(image)
    metadata_path = path / "template.json"
    if not metadata_path.exists():
        raise FileNotFoundError(f"No local template image found at {path}")
    metadata = TemplateMetadata.load(metadata_path)
    return metadata, path

def list_local_images() -> List[TemplateImage]:
    root = Path.home() / ".cache" / "new" / "templates"
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

