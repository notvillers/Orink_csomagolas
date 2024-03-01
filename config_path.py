'''Paths'''

import os
import socket

path = os.path.dirname(__file__)

CONFIG_JSON_SUBPATH = "config"
CONFIG_JSON_NAME = "config.json"
config_json_path = os.path.join(path, CONFIG_JSON_SUBPATH, CONFIG_JSON_NAME)
FTP_JSON_NAME = "ftp.json"
ftp_json_path = os.path.join(path, CONFIG_JSON_SUBPATH, FTP_JSON_NAME)

if not os.path.exists(os.path.join(path, CONFIG_JSON_SUBPATH)):
    os.makedirs(os.path.join(path, CONFIG_JSON_SUBPATH))

DB_SUBPATH = "db"
hostname = socket.gethostname()
db_name = hostname + "_log.db"
db_path = os.path.join(path, DB_SUBPATH, db_name)

if not os.path.exists(os.path.join(path, DB_SUBPATH)):
    os.makedirs(os.path.join(path, DB_SUBPATH))

TEMP_DIR = "temp"
temp_path = os.path.join(path, TEMP_DIR)
BP_INTERVAL_S = 120

if not os.path.exists(os.path.join(path, TEMP_DIR)):
    os.makedirs(os.path.join(path, TEMP_DIR))

ICON_SUBPATH = "src"
ICON_NAME = "icon.ico"
icon_path = os.path.join(path, ICON_SUBPATH, ICON_NAME)
USERS_NAME = "users.csv"
users_path = os.path.join(path, ICON_SUBPATH, USERS_NAME)
