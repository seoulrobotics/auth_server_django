import os
import json


def get_configs():
    CONFIG_FILE_PATH = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), "config.json")
    with open(CONFIG_FILE_PATH, 'r') as file:
        config = json.load(file)
        return config