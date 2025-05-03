import json
from pathlib import Path
from typing import List

class TemplateRegistry:
    def __init__(self, template_paths: List[Path]) -> None:
        self.template_paths = [Path(p).expanduser().resolve() for p in template_paths]
        self.registry = self._load_all_templates()

    def _load_all_templates(self):
        full_registry = {}
        for path in self.template_paths:
            index = path / "templates.json"
            if not index.exists():
                continue
            with index.open("r") as f:
                try:
                    data = json.load(f)
                    full_registry[path] = data
                except json.JSONDecodeError:
                    print(f"Invalid JSON in {index}")
        return full_registry

    def get_template(self, type_: str, name: str):
        for base_path, data in self.registry.items():
            if type_ in data and name in data[type_]:
                meta = data[type_][name]
                template_folder = base_path / meta['path']
                if template_folder.exists():
                    return meta, template_folder
        raise FileNotFoundError(f"Template '{type_}/{name}' not found in any configured template path")
