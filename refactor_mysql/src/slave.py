'''slave functions'''

from datetime import datetime
import uuid
import json

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
