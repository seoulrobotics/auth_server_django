import json
from json.decoder import JSONDecodeError
import os
import sys
from django.core.management.utils import get_random_secret_key
import shutil

#config given by SENSR
INIT_CONFIG_FILE_PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "init_config.json")

#generated config from this script
CONFIG_FILE_PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "config.json")

TEMPLATE_DB = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "db_template.sqlite3")

DB_PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "db.sqlite3")

TEMPLATE_SERVICE = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "sr_auth.service.template")

SERIVCE_PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "sr_auth.service")

def get_configs():
    with open(CONFIG_FILE_PATH, 'r') as file:
        try:
            config = json.load(file)
            return config
        except JSONDecodeError:
            return {}

def init_configs():
    with open(INIT_CONFIG_FILE_PATH, 'r') as file:
        config = json.load(file)
    # create new secret key and overwrite
    config["SECRET_KEY"] = get_random_secret_key()
    
    config["SR_TRUSTED_DOMAINS"] = [
        "http://127.0.0.1:3000", "http://127.0.0.1:9020"]
    
    config["SR_TRUSTED_DOMAINS"] = list(
        dict.fromkeys(config["SR_TRUSTED_DOMAINS"]))
    
    # overwrite
    if os.path.exists(CONFIG_FILE_PATH):
        os.remove(CONFIG_FILE_PATH)
    with open(CONFIG_FILE_PATH, 'w+') as file:
        try:
            config = file.write(json.dumps(config, indent=4))
        except JSONDecodeError:
            raise Exception("Failed to create auth server config")


def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    shutil.copyfile(TEMPLATE_DB, DB_PATH)


def create_service_file():
    if os.path.exists(SERIVCE_PATH):
        os.remove(SERIVCE_PATH)
    with open(TEMPLATE_SERVICE, 'r') as file:
        service_script = file.read()
    service_script = service_script.replace(
        'SERVER_CMD', f'python3 { os.path.join(os.path.dirname(__file__),"manage.py")} runserver')
    with open(SERIVCE_PATH, 'w+') as file:
        try:
            file.write(service_script)
        except JSONDecodeError:
            raise Exception("Failed to create auth server service file")

    

if __name__ == "__main__":
    init_configs()
    init_db()
