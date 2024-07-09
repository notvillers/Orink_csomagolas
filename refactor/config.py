'''config file'''

import sys
import os
import socket
from villog import Logger

path: str = os.path.dirname(__file__)
db_dir: str = os.path.join(path, "db")
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
db_name: str = socket.gethostname() + ".db"
db_path: str = os.path.join(path, db_dir, db_name)

json_dir: str = os.path.join(path, "json")
if not os.path.exists(json_dir):
    os.makedirs(json_dir)
usercode_json: str = os.path.join(json_dir, "usercode.json")

data_dir: str = os.path.join(path, "data")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

user_csv_path: str = os.path.join(data_dir, "users.csv")

venv_dir: str = os.path.join(path, ".venv")
if not os.path.exists(venv_dir):
    Logger().log(f"{venv_dir} not found, exiting...")
    sys.exit(1)

ftp_path: str = os.path.join(venv_dir, "ftp.json")
if not os.path.exists(ftp_path):
    Logger().log(f"{ftp_path} not found, exiting...")
    sys.exit(1)
