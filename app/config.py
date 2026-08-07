import json
import os
import shutil

from pathlib import Path


APP_NAME = "autoclicker"

DEFAULT_CONFIG = {
    "interval": 0.1,
    "button": 1,
    "amount": 0,
    "hotkey": "f6"
}


def _xdg_config_home() -> Path:
    env = os.environ.get("XDG_CONFIG_HOME")
    if env:
        return Path(env)
    return Path.home() / ".config"


def _config_dir() -> Path:
    return _xdg_config_home() / APP_NAME


def _config_file() -> Path:
    return _config_dir() / "config.json"


def _legacy_config_file() -> Path:
    return Path(__file__).parent.parent / "config.json"


def _migrate_if_needed():
    new = _config_file()
    old = _legacy_config_file()
    if new.exists() or not old.exists():
        return
    try:
        _config_dir().mkdir(parents=True, exist_ok=True)
        shutil.copy2(old, new)
    except OSError:
        pass


def load_config():
    _migrate_if_needed()
    config_file = _config_file()

    if not config_file.exists():
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    try:
        with open(config_file, "r") as file:
            config = json.load(file)
    except (json.JSONDecodeError, OSError):
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    if not isinstance(config, dict):
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    merged = dict(DEFAULT_CONFIG)
    merged.update(config)

    return merged


def save_config(config):
    config_file = _config_file()
    config_file.parent.mkdir(parents=True, exist_ok=True)

    with open(config_file, "w") as file:
        json.dump(
            config,
            file,
            indent=4
        )
