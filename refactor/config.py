'''config file'''

import os
import socket

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