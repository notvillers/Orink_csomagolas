import config_path
import os
import json

config_json = config_path.config_json_path

def create_config(name: str = config_json):
    if not os.path.exists(name):
        data = {
            "usercode": 0000
        }
        with open(name, "w", encoding = "utf-8") as file:
            json.dump(data, file, indent = 2)
        return True
    return False

def config_read(name: str = config_json):
    if os.path.exists(name):
        with open(name, "r", encoding = "utf-8") as file:
            data = json.load(file)
        return data
    return False

def config_update(name: str = config_json, usercode: str = None):
    if os.path.exists(name):
        with open(name, "r", encoding = "utf-8") as file:
            data = json.load(file)
        data["usercode"] = (usercode if usercode != None else data["usercode"])
        with open(name, "w", encoding = "utf-8") as file:
            json.dump(data, file, indent = 2)
        return True
    return False