'''cleaner'''

import os
from config import log_path, temp_path
from src.slave import date_str
from villog import Logger

l = Logger(
    file_path = os.path.join(log_path, f"cleaner_{date_str()}.log")
)

def clean_folder_content(folder: str) -> None:
    '''Clean the content of a folder'''
    for file in os.listdir(folder):
        file_path: str = os.path.join(folder, file)
        if os.path.isfile(file_path):
            l.log(f"Trying to remove: {file_path}")
            try:
                os.remove(file_path)
                l.log(f"Removed: {file_path}")
            except Exception as e:
                    l.log(e)

if __name__ == "__main__":
    l.log("Cleaner started")
    clean_folder_content(temp_path)
    l.log("Cleaner finished")