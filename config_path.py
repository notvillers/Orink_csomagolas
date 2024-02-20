import os
import socket

path = os.path.dirname(__file__)
version = "0.1"

config_json_subpath = "config"
config_json_name = "config.json"
config_json_path = os.path.join(path, config_json_subpath, config_json_name)

if not os.path.exists(os.path.join(path, config_json_subpath)):
    os.makedirs(os.path.join(path, config_json_subpath))

db_subpath = "db"
hostname = socket.gethostname()
db_name = hostname + "_log.db"
db_path = os.path.join(path, db_subpath, db_name)

if not os.path.exists(os.path.join(path, db_subpath)):
    os.makedirs(os.path.join(path, db_subpath))