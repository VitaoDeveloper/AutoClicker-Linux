import json
import os


from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

CONFIG_FILE = BASE_DIR / "config.json"


DEFAULT_CONFIG = {
    "interval": 0.1,
    "button": 1,
    "amount": 0,
    "hotkey": "f6"
}


def load_config():

    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    except (json.JSONDecodeError, OSError):
        # Arquivo corrompido ou ilegível: restaura o padrão
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    if not isinstance(config, dict):
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    # Garante que chaves ausentes (config antigo/incompleto) usem o padrão
    merged = dict(DEFAULT_CONFIG)
    merged.update(config)

    return merged



def save_config(config):

    with open(CONFIG_FILE, "w") as file:
        json.dump(
            config,
            file,
            indent=4
        )
