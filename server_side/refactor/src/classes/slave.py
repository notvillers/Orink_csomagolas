'''slave class'''

import os
import shutil
import src.sql.sqlite as sqlite_q
import src.sql.o8 as o8_q

class SqliteQuery:
    '''sqlite query class'''
    csomag_create: str = sqlite_q.CSOMAG_TABLE_CREATE
    csomag_insert: str = sqlite_q.CSOMAG_TABLE_INSERT
    csomag_delete: str = sqlite_q.CSOMAG_TABLE_DELETE
    csomag_select_all: str = sqlite_q.CSOMAG_TABLE_SELECT_ALL
    osszesito_create: str = sqlite_q.OSSZESITO_TABLE_CREATE
    osszesito_insert_from_csomag: str = sqlite_q.OSSZESITO_TABLE_INSERT_FROM_CSOMAG
    osszesito_select_csomagszam_without_date: str = sqlite_q.OSSZESITO_SELECT_CSOMAGSZAM_WITHOUT_O8DATE
    osszesito_update_crdti: str = sqlite_q.OSSZESITO_UPDATE_CRDTI
    user_create: str = sqlite_q.USER_CREATE
    user_insert: str = sqlite_q.USER_INSERT
    user_select: str = sqlite_q.USER_SELECT
    xlsx_osszesito_select: str = sqlite_q.XLSX_OSSZESITO_SELECT
    select_user_with_csomag: str = sqlite_q.SELECT_USERS_WITH_CSOMAG
    select_username_for_usercode: str = sqlite_q.SELECT_USERNAME_FOR_USERCODE
    select_csomag_for_user: str = sqlite_q.SELECT_CSOMAG_FOR_USER

class O8Query:
    '''o8 query class'''
    select_crdti_by_csomagszam: str = o8_q.SELECT_CRDTI_BY_CSOMAGSZAM
    select_users: str = o8_q.SELECT_USERS

class Slave:
    '''slave class'''

    def __init__(self) -> None:
        self.sqlite = SqliteQuery()
        self.o8 = O8Query()

    def list_files(self, directory: str) -> list:
        '''list files in a directory'''
        files = os.listdir(directory)
        return files

    def list_files_with_extension(self, directory: str, extension: str) -> list:
        '''list files with extension'''
        files = os.listdir(directory)
        extension = extension if extension.startswith(".") else f".{extension}"
        return [os.path.join(directory, file) for file in files if file.lower().endswith(extension.lower())]

    def copy_file(self, source: str, destination: str) -> None:
        '''copy file'''
        shutil.copy(source, destination)
