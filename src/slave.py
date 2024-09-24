'''slave functions'''

from datetime import datetime
import uuid
import json
import os

def date_str() -> str:
    '''Return the current date and time as a string'''
    return datetime.now().strftime("%Y-%m-%d")

def gen_uuid() -> str:
    '''Generate a unique identifier'''
    return str(uuid.uuid4())

def read_json(file_path: str, encoding: str = "utf-8-sig") -> dict:
    '''read json file'''
    with open(file_path, "r", encoding = encoding) as file:
        return json.load(file)

def read_file(file_path: str, encoding: str = "utf-8-sig") -> str:
    '''read file'''
    with open(file_path, "r", encoding = encoding) as file:
        return file.read()

def get_files_in_dir(dir_path: str) -> list:
    '''get files in directory'''
    return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

def delete_file(file_path: str) -> None:
    '''delete file'''
    os.remove(file_path)

def delete_all_file_in_dir(dir_path: str) -> None:
    '''delete all files in directory'''
    for f in get_files_in_dir(dir_path):
        delete_file(os.path.join(dir_path, f))
