'''File handling'''

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
        return False

def clean_dir(directory_path: str):
    '''removes files from a dir'''
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    text_to_log(file_path + " removed")
                    return True
                return False
            except Exception as e:
                text_to_log(str(e))
                return False
    return False

def read_csv(file_name: str):
    '''reads a csv'''
    if os.path.exists(file_name):
        with open(file_name, "r", encoding = "utf-8") as file:
            lines_list = [line.strip() for line in file]
        return lines_list
    return False

def csv_user_format(csv_list: list):
    '''formats csv
    "," -> " - "'''
    new_list = []
    for row in csv_list:
        row_split = row.replace(",", " - ")
        new_list.append(row_split)
    return new_list

def csv_tuple(csv_list: list):
    '''creates a tuple from the csv'''
    new_list = []
    for row in csv_list:
        row_split = row.split(",")
        new_list.append(row_split)
    return new_list
