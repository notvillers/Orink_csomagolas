'''Handles the .jsons'''

import json
import os
import sys
import config_path
from funct.log import text_to_log

LOGIN_JSON = config_path.login_path
FTP_JSON = config_path.ftp_path

# Creating login.json if not found
def login_db_create(json_file = LOGIN_JSON):
    '''creates login.json'''
    if not os.path.exists(json_file):
        data = {
            "server": "server_name", # Name of your server
            "database": "database_name", # Name of your database
            "username": "yourusername", # SQL username
            "password": "yourpassword", # SQL password
        }
        with open(json_file, 'w', encoding = "utf-8") as file:
            json.dump(data, file, indent = 2)
        text_to_log(json_file + " generated...")
        return True

    return False

# Reading .json
def json_read(json_file):
    '''reads .json'''
    if os.path.exists(json_file):
        with open(json_file, "r", encoding = "utf-8") as file:
            data = json.load(file)
        return data
    return False

# Creating .json if not found
if login_db_create():
    text_to_log("Please fill out the generated .json(s)!")
    sys.exit()

# Creates ftp.json
def create_ftp(name: str = FTP_JSON):
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
def ftp_read(name: str = FTP_JSON):
    '''reads ftp.json'''
    if os.path.exists(name):
        with open(name, "r", encoding = "utf-8") as file:
            data = json.load(file)
        return data
    return False

def ftp_update(name: str = FTP_JSON, hostname: str = None, username: str = None, password: str = None, directory: str = None):
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