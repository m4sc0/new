from collections import defaultdict
import json
import os
from pathlib import Path
from typing import List, Tuple

CONFIG_PATH = Path.home() / ".config" / "new" / "config.json"
DEFAULT_CONFIG = {
    "template_paths": [],
    "open_main_file": False,
    "remote": "https://repo.new.kackhost.de",
    "allow_missing_version": True,
    "upload_token": "no-token"
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
            for k, v in DEFAULT_CONFIG.items():
                if k not in self._config:
                    self._config[k] = v
            self._write()

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

    def get_allow_missing_version(self) -> bool:
        return self._config.get("allow_missing_version", DEFAULT_CONFIG["allow_missing_version"])

    def set_allow_missing_version(self, allow: bool):
        self._config["allow_missing_version"] = allow
        self._write()

    def get_upload_token(self):
        token = self._config.get("upload_token", "no-token")
        if token == "no-token":
            return False, ""
        return True, token

    def set_upload_token(self, token: str):
        self._config["upload_token"] = token
        self._write()

    def reload(self):
        self._load_or_initialize()

    def get_config(self):
        return self._config.copy()

config = Config()
