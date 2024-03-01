'''Configs'''

import os

path = os.path.dirname(__file__)

DB_USBPATH = "db"
DB_NAME = "csomagolas.db"
db_path = os.path.join(path, DB_USBPATH, DB_NAME)

if not os.path.exists(os.path.join(path, DB_USBPATH)):
    os.makedirs(os.path.join(path, DB_USBPATH))

LOGS_SUBPATH = "logs"
logs_path = os.path.join(path, LOGS_SUBPATH)

if not os.path.exists(os.path.join(path, LOGS_SUBPATH)):
    os.makedirs(os.path.join(path, LOGS_SUBPATH))

TEMP_SUBPATH = "temp"
temp_path = os.path.join(path, TEMP_SUBPATH)

if not os.path.exists(os.path.join(path, TEMP_SUBPATH)):
    os.makedirs(os.path.join(path, TEMP_SUBPATH))

LOGIN_JSON = "login.json"
login_path = os.path.join(path, LOGIN_JSON)
