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
BP_INTERVAL_M = 5

if not os.path.exists(os.path.join(path, TEMP_DIR)):
    os.makedirs(os.path.join(path, TEMP_DIR))

ICON_SUBPATH = "src"
ICON_NAME = "icon.ico"
icon_path = os.path.join(path, ICON_SUBPATH, ICON_NAME)
ICON_MACOS_NAME = "icon.png"
icon_macos_path = os.path.join(path, ICON_SUBPATH, ICON_MACOS_NAME)
USERS_NAME = "users.csv"
users_path = os.path.join(path, ICON_SUBPATH, USERS_NAME)
INFO_ICON = "info.png"
info_path = os.path.join(path, ICON_SUBPATH, INFO_ICON)

# Others

# Events
'''
    "key": "key to press",
    "event": "event it generates"
'''

EVENT_KEYS = [
    {"key": ["<Escape>"], "event": "-ESCAPE-", "info": None}, # esc
    {"key": ["<Control-Key>"], "event": "-ctrl-", "info": "CTRL: Gyorsgombok (Kizárólag MacOS)"}, # ctrl
    {"key": ["<Control-a>", "<Control-A>"], "event": "-ctrl_a-", "info": "CTRL+A: Adatok"}, # ctrl+a
    {"key": ["<Control-e>", "<Control-E>"], "event": "-ctrl_e-", "info": "CTRL+E: Eseménynapló"}, # ctrl+e
    {"key": ["<Control-f>", "<Control-F>"], "event": "-ctrl_f-", "info": "CTRL+F: Feltöltés"}, # ctrl+f
    {"key": ["<Control-i>", "<Control-I>"], "event": "-ctrl_i-", "info": "CTRL+I: Infó (ez az ablak)"}, # ctrl+i
    {"key": ["<Control-r>", "<Control-R>"], "event": "-ctrl_r-", "info": "CTRL+R: Újratöltés (rendszergazda mód)"}, # ctrl+r
    {"key": ["<Control-s>", "<Control-S>"], "event": "-ctrl_s-", "info": "CTRL+S: Rendszergazda mód"}, # ctrl+s
]