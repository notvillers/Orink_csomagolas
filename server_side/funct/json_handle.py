# Handles the .jsons

import config_path
import json
import os
import sys
from funct.log import text_to_log

# Creating login.json if not found
def login_db_create(json_file = config_path.login_path):
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
    if os.path.exists(json_file):
        with open(json_file, "r", encoding = "utf-8") as file:
            data = json.load(file)
        return data
    return False

# Creating .json if not found
if login_db_create():
    text_to_log("Please fill out the generated .json(s)!")
    sys.exit()