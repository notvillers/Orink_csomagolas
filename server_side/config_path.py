# Configs

import os

path = os.path.dirname(__file__)

db_subpath = "db"
db_name = "csomagolas.db"
db_path = os.path.join(path, db_subpath, db_name)

if not os.path.exists(os.path.join(path, db_subpath)):
    os.makedirs(os.path.join(path, db_subpath))

logs_subpath = "logs"

if not os.path.exists(os.path.join(path, logs_subpath)):
    os.makedirs(os.path.join(path, logs_subpath))