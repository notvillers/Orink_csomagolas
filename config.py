'''config.py: Configuration file for the project'''

import os

def create_on_not_found(path: str) -> bool:
    '''Create a directory if it doesn't exist'''
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory created: {path}")
        return True
    print(f"Directory already exists: {path}")
    return False

def exit_on_not_found(path: str) -> bool:
    '''Exit the program if a directory does not exist'''
    if not os.path.exists(path):
        print(f"Directory not found: {path}")
        exit(1)
    print(f"Directory found: {path}")
    return True

path: str = os.path.dirname(__file__)

VENV_DIR: str = ".venv"
venv_path: str = os.path.join(path, VENV_DIR)
exit_on_not_found(venv_path)

o8_json: str = os.path.join(venv_path, "o8.json")
exit_on_not_found(o8_json)

maria_json: str = os.path.join(venv_path, "maria.json")
exit_on_not_found(maria_json)

LOG_DIR: str = "log"
log_path: str = os.path.join(path, LOG_DIR)
create_on_not_found(log_path)

TEMP_DIR: str = "temp"
temp_path: str = os.path.join(path, TEMP_DIR)
create_on_not_found(temp_path)

SRC_DIR: str = "src"
src_path: str = os.path.join(path, SRC_DIR)
exit_on_not_found(src_path)

SQL_DIR: str = "sql"
sql_path: str = os.path.join(src_path, SQL_DIR)
exit_on_not_found(sql_path)

O8_PACKAGE_CHECK: str = "o8_package_check.sql"
O8_PACKAGE_CHECK_PATH: str = os.path.join(sql_path, O8_PACKAGE_CHECK)
exit_on_not_found(O8_PACKAGE_CHECK_PATH)

DEFAULT_USERCODE: int = 2

WORK_STATES: dict[int, str] = {
    1: "Csomagolás",
    2: "Pakolás",
    3: "Egyéb munkavégzés",
}
