import json
import os


CONFIG_FILE = "config.json"


DEFAULT_CONFIG = {
    "interval": 0.1,
    "button": 1,
    "amount": 0
}


def load_config():

    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG


    with open(CONFIG_FILE, "r") as file:
        return json.load(file)



def save_config(config):

    with open(CONFIG_FILE, "w") as file:
        json.dump(
            config,
            file,
            indent=4
        )