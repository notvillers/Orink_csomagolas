'''Json handler'''

import os
import json
import config_path

config_json = config_path.config_json_path
ftp_json = config_path.ftp_json_path

# Creates config.json
def create_config(name: str = config_json):
    '''creates config.json'''
    if not os.path.exists(name):
        data = {
            "usercode": 2
        }
        with open(name, "w", encoding = "utf-8") as file:
            json.dump(data, file, indent = 2)
        return True
    return False

# Reads config.json
def config_read(name: str = config_json):
    '''reads config.json'''
    if os.path.exists(name):
        with open(name, "r", encoding = "utf-8") as file:
            data = json.load(file)
        return data
    return False

# Updaters config.json
def config_update(name: str = config_json, usercode: str = None):
    '''updates config.json'''
    if os.path.exists(name):
        with open(name, "r", encoding = "utf-8") as file:
            data = json.load(file)
        data["usercode"] = (usercode if usercode is not None else data["usercode"])
        with open(name, "w", encoding = "utf-8") as file:
            json.dump(data, file, indent = 2)
        return True
    return False

# Creates ftp.json
def create_ftp(name: str = ftp_json):
    '''creates ftp.json'''
    if not os.path.exists(name):
        data = {
            "hostname": "your_server",
            "username": "your_username",
            "password": "your_password",
            "directory": "your_directory"
        }
        with open(name, "w", encoding = "utf-8") as file:
            json.dump(data, file, indent = 2)
        return True
    return False

# Reads ftp.json
def ftp_read(name: str = ftp_json):
    '''reads ftp.json'''
    if os.path.exists(name):
        with open(name, "r", encoding = "utf-8") as file:
            data = json.load(file)
        return data
    return False

def ftp_update(name: str = ftp_json, hostname: str = None, username: str = None, password: str = None, directory: str = None):
    '''updates ftp.json'''
    if os.path.exists(name):
        with open(name, "r", encoding = "utf-8") as file:
            data = json.load(file)
        data["hostname"] = (hostname if hostname is not None else data["hostname"])
        data["username"] = (username if username is not None else data["username"])
        data["password"] = (password if password is not None else data["password"])
        data["directory"] = (directory if directory is not None else data["directory"])
        with open(name, "w", encoding= "utf-8") as file:
            json.dump(data, file, indent = 2)
        return True
    return False
