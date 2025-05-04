from pathlib import Path
import json
from typing import List, Optional


class TemplateMetadata:
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        placeholders: Optional[List[str]] = None,
        open_file: Optional[str] = None,
        category: Optional[str] = None,
        version: Optional[str] = None
    ) -> None:
        self.name = name
        self.description = description
        self.placeholders = placeholders or []
        self.open = open_file
        self.category = category
        self.version = version

    @classmethod
    def load(cls, path: Path) -> "TemplateMetadata":
        if not path.exists():
            raise FileNotFoundError(f"template.json not found: {path}")

        with path.open("r") as f:
            data = json.load(f)

        return cls(
            name=data.get("name"),
            description=data.get("description"),
            placeholders=data.get("placeholders", []),
            open_file=data.get("open"),
            category=data.get("category"),
            version=data.get("version")
        )

    def template(self) -> str:
        return f"{self.category}/{self.name}:{self.version}"

    def dump(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "placeholders": self.placeholders,
            "open": self.open,
            "category": self.category,
            "version": self.version
        }

    def save(self, path: Path):
        with path.open("w") as f:
            json.dump(self.dump(), f, indent=2)

    def __str__(self):
        return f"{self.category}/{self.name}:{self.version or 'N/A'} - {self.description or ''}"

