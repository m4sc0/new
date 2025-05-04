import json
import os
from pathlib import Path
from typing import List

CONFIG_PATH = Path.home() / ".config" / "new" / "config.json"
DEFAULT_CONFIG = {
    "template_paths": [],
    "open_main_file": False,
    "remote": "https://repo.new.kackhost.de"
}

class Config:
    def __init__(self) -> None:
        self._config = {}
        self._load_or_initialize()

    def _load_or_initialize(self):
        if not CONFIG_PATH.exists():
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            self._config = DEFAULT_CONFIG.copy()
            self._write()
        else:
            with CONFIG_PATH.open("r") as f:
                self._config = json.load(f)

    def _write(self):
        with CONFIG_PATH.open("w") as f:
            json.dump(self._config, f, indent=2)

    def get_template_paths(self) -> List[Path]:
        # create fallback folder if not existing
        fallback_template_folder = Path.home() / ".config" / "new" / "templates"
        fallback_template_folder.mkdir(parents=True, exist_ok=True)

        full_paths = self._config.get("template_paths", [])
        full_paths.append(fallback_template_folder.resolve())

        full_paths = [Path(p).expanduser().resolve() for p in full_paths]

        return full_paths

    def add_template_path(self, path: str):
        if path not in self._config["template_paths"]:
            self._config["template_paths"].append(path)
            self._write()

    def get_open_main_file(self) -> bool:
        return self._config.get("open_main_file", False)

    def set_open_main_file(self, value: bool):
        self._config["open_main_file"] = value
        self._write()

    def get_remote_url(self) -> str:
        return self._config.get("remote", DEFAULT_CONFIG["remote"])

    def set_remote_url(self, url: str):
        self._config["remote"] = url
        self._write()

    def reload(self):
        self._load_or_initialize()

    def get_config(self):
        return self._config.copy()

config = Config()
