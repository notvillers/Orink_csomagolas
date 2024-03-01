'''file handler'''

import shutil
import os
from funct.log import text_to_log

def copy(source_file: str, destination_file: str):
    '''copies a file'''
    try:
        shutil.copy(source_file, destination_file)
        return source_file + " -> " + destination_file
    except Exception as e:
        text_to_log(str(e))

def clean_dir(directory_path: str):
    '''cleans a dir'''
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    text_to_log(file_path + " removed")
            except Exception as e:
                text_to_log(str(e))

def ls(directory_path: str):
    '''lists files in dir'''
    files = os.listdir(directory_path)
    return files

def ls_with_path(directory_path: str):
    '''lists files in dir with absolute path'''
    files = os.listdir(directory_path)
    files_with_path = []
    for file in files:
        files_with_path.append(os.path.join(directory_path, file))
    return files_with_path