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


def get_filename_from_path(file_path: str):
    '''returns the filename from a full path'''
    return os.path.basename(file_path)


def reorder_matrix(matrix, column):
    '''reorders the matrix based on a specified column'''
    matrix.sort(key=lambda row: row[column])
    text_to_log("matrix reordered")
    return matrix


def matrix_to_list(matrix, separator: str = ","):
    '''creates a list from a matrix by joining row elements with ","'''
    result = []
    for row in matrix:
        if isinstance(row, int):
            result.append(str(row))
        else:
            result.append(separator.join(str(item) for item in row))
    text_to_log("matrix converted to list")
    return result


def write_list_to_file(file_path, data):
    '''writes a list into a file'''
    with open(file_path, "w", encoding = "utf-8") as file:
        for item in data:
            file.write(str(item) + "\n")
    text_to_log("list written to " + file_path)
    return file_path