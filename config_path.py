# Configs

import os
import socket

path = os.path.dirname(__file__)

config_json_subpath = "config"
config_json_name = "config.json"
config_json_path = os.path.join(path, config_json_subpath, config_json_name)
ftp_json_name = "ftp.json"
ftp_json_path = os.path.join(path, config_json_subpath, ftp_json_name)

if not os.path.exists(os.path.join(path, config_json_subpath)):
    os.makedirs(os.path.join(path, config_json_subpath))

db_subpath = "db"
hostname = socket.gethostname()
db_name = hostname + "_log.db"
db_path = os.path.join(path, db_subpath, db_name)

if not os.path.exists(os.path.join(path, db_subpath)):
    os.makedirs(os.path.join(path, db_subpath))

temp_dir = "temp"
temp_path = os.path.join(path, temp_dir)
backup_interval_s = 120

if not os.path.exists(os.path.join(path, temp_dir)):
    os.makedirs(os.path.join(path, temp_dir))
    
icon_subpath = "src"
icon_name = "icon.ico"
icon_path = os.path.join(path, icon_subpath, icon_name)