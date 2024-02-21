import config_path
import shutil
import os
from funct.log import text_to_log

def copy(source_file: str, destination_file: str):
    try:
        shutil.copy(source_file, destination_file)
        return source_file + " -> " + destination_file
    except Exception as e:
        text_to_log(str(e))

def clean_dir(directory_path: str):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    text_to_log(file_path + " removed")
            except Exception as e:
                text_to_log(str(e))