'''Paths'''

import os
import socket

# OS check
IS_MACOS = (os.name == 'posix' and os.uname().sysname == 'Darwin')
IS_LINUX = (os.name == 'posix' and os.uname().sysname == 'Linux')

path = os.path.dirname(__file__)

CONFIG_JSON_SUBPATH = "config"
CONFIG_JSON_NAME = "config.json"
config_json_path = os.path.join(path, CONFIG_JSON_SUBPATH, CONFIG_JSON_NAME)
FTP_JSON_SUBPATH = os.path.join(".venv")
FTP_JSON_NAME = "ftp.json"
ftp_json_path = os.path.join(path, FTP_JSON_SUBPATH, FTP_JSON_NAME)

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

# Others

# Events
'''
    "key": "key to press",
    "event": "event it generates"
'''
EVENT_KEYS = [
    {"key": "<Escape>", "event": "-ESCAPE-"}, # esc
    {"key": "<Control-Key>", "event": "-ctrl-"}, # ctrl
    {"key": "<Control-a>", "event": "-ctrl_a-"}, # ctrl+a
    {"key": "<Control-A>", "event": "-ctrl_a-"}, # ctrl+A
    {"key": "<Control-e>", "event": "-ctrl_e-"}, # ctrl+e
    {"key": "<Control-f>", "event": "-ctrl_f-"}, # ctrl+f
    {"key": "<Control-F>", "event": "-ctrl_f-"}, # ctrl+F
    {"key": "<Control-e>", "event": "-ctrl_e-"}, # ctrl+e
    {"key": "<Control-E>", "event": "-ctrl_e-"}, # ctrl+E
    {"key": "<Control-r>", "event": "-ctrl_r-"}, # ctrl+r
    {"key": "<Control-R>", "event": "-ctrl_r-"}, # ctrl+R
    {"key": "<Control-s>", "event": "-ctrl_s-"}, # ctrl+s
    {"key": "<Control-S>", "event": "-ctrl_s-"} # ctrl+S
]