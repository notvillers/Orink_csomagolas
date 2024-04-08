'''clean up'''

import os
from funct.log import text_to_log
from config_path import DB_USBPATH, LOGS_SUBPATH, BACKUP_SUBPATH, TEMP_SUBPATH

PATHS_TO_CLEAN = [DB_USBPATH, LOGS_SUBPATH, BACKUP_SUBPATH, TEMP_SUBPATH]

def clean_folder(path: str):
    '''cleans the db folder'''
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            text_to_log("removed " + file_path)


def main():
    '''main'''
    text_to_log("cleaning up")
    for path in PATHS_TO_CLEAN:
        clean_folder(path)


if __name__ == "__main__":
    main()
