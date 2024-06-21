'''MAIN'''

import os
import config_path
from funct.sqlite_handle import Connection as sqlite_connection
import funct.db_config
import funct.file_handle
import funct.xlsx_handle
import funct.json_handle
from funct.octopus_handle import Octopus8_sql as octopus_client_class
import funct.data_config
from funct.ftp_handle import Client as ftp_client_class
from funct.slave import current_datetime_to_string
from funct.log import text_to_log

# sqlite query
CSOMAG_TABLE_CREATE = funct.db_config.CSOMAG_TABLE_CREATE
OSSZESITO_TABLE_CREATE = funct.db_config.OSSZESITO_TABLE_CREATE
CSOMAG_TABLE_SELECT = funct.db_config.CSOMAG_TABLE_SELECT
CSOMAG_TABLE_INSERT = funct.db_config.CSOMAG_TABLE_INSERT
OSSZESITO_TABLE_INSERT_FROM_CSOMAG = funct.db_config.OSSZESITO_TABLE_INSERT_FROM_CSOMAG
OSSZESITO_TABLE_SELECT_DISTINCT_USERS = funct.db_config.OSSZESITO_TABLE_SELECT_DISTINCT_USERS
OSSZESITO_SELECT_BY_USER = funct.db_config.OSSZESITO_SELECT_BY_USER
OSSZESITO_TABLE_SELECT = funct.db_config.OSSZESITO_TABLE_SELECT
OSSZESITO_UPDATE_O8_CONFIRM = funct.db_config.OSSZESITO_UPDATE_O8_CONFIRM
OSSZESITO_SELECT_CONFIRMED = funct.db_config.OSSZESITO_SELECT_CONFIRMED
OSSZESITO_UPDATE_O8_CRDTI = funct.db_config.OSSZESITO_UPDATE_O8_CRDTI
USER_TABLE_CREATE = funct.db_config.USER_TABLE_CREATE
USER_TABLE_DELETE_ALL = funct.db_config.USER_TABLE_DELETE_ALL
USER_TABLE_INSERT = funct.db_config.USER_TABLE_INSERT
XLSX_OSSZESITO_SELECT = funct.db_config.XLSX_OSSZESITO_SELECT
USER_SELECT_BY_USERCODE = funct.db_config.USER_SELECT_BY_USERCODE

# octopus query
O8_SELECT_USERNAME_BY_USERCODE = funct.db_config.O8_SELECT_USERNAME_BY_USERCODE
O8_SELECT_INFO_BY_CSOMAGSZAM = funct.db_config.O8_SELECT_INFO_BY_CSOMAGSZAM
O8_SELECT_CRDTI_BY_CSOMAGSZAM = funct.db_config.O8_SELECT_CRDTI_BY_CSOMAGSZAM
O8_SELECT_USERS_FOR_CSV = funct.db_config.O8_SELECT_USERS_FOR_CSV

# config
FTP_INFO = funct.json_handle.ftp_read()
OCTOPUS_INFO = funct.json_handle.json_read(config_path.login_path)
LOGS_PATH = config_path.logs_path
BACKUP_PATH = config_path.backup_path
DL_PATH = [LOGS_PATH, BACKUP_PATH]

def create_ftp_client(hostname: str, username: str, password: str):
    '''creates ftp client'''
    return ftp_client_class(hostname, username, password)

def download_all_db_files(ftp_client: ftp_client_class, namelike: str, path: str):
    '''downloads all db files from ftp'''
    ftp_client.download_all_db_files(namelike, path)
    return True

def download_all_db_files_by_path(ftp_client: ftp_client_class, dl_path: list, namelike: str):
    '''downloads all db files from ftp'''
    if dl_path:
        for path in dl_path:
            download_all_db_files(ftp_client, namelike, path)
        return True
    return False

def create_o8_client(octopus_info: dict):
    '''creates octopus client'''
    return octopus_client_class(octopus_info)

def create_db_client():
    '''creates db client'''
    return sqlite_connection()

def main():
    '''main'''

    # FTP connection
    ftp_client = create_ftp_client(FTP_INFO["hostname"], FTP_INFO["username"], FTP_INFO["password"])

    # Downloading db files
    download_all_db_files_by_path(ftp_client, DL_PATH, FTP_INFO["directory"])

    # Octopus 8 connection
    o8_client = create_o8_client(OCTOPUS_INFO)

    # main db connection
    db_client = create_db_client()
    db_client.execute(CSOMAG_TABLE_CREATE)
    db_client.execute(OSSZESITO_TABLE_CREATE)
    db_client.execute(USER_TABLE_CREATE)

    # Importing users from Octopus 8
    columns, results = o8_client.execute(O8_SELECT_USERS_FOR_CSV)
    for result in results:
        db_client.execute(USER_TABLE_INSERT, result)

    # Creating users.csv
    if results:
        sort_results = funct.file_handle.reorder_matrix(results, 1)
        results_csv = funct.file_handle.matrix_to_list(sort_results)
        user_csv_path = funct.file_handle.write_list_to_file(os.path.join(config_path.temp_path, "users.csv"), results_csv)
        ftp_client.upload(user_csv_path, "src", "users.csv")

    # getting .db files
    files = funct.file_handle.ls_with_path(os.path.join(config_path.path, config_path.LOGS_SUBPATH))

    # merging .db files
    for file in files:
        cache_db = sqlite_connection(file)
        columns, result = cache_db.select(CSOMAG_TABLE_SELECT)
        for row in result:
            db_client.insert(CSOMAG_TABLE_INSERT, (row[0], row[1], os.path.basename(file), row[2]))
        cache_db.close()
        os.remove(file)

    # creating distinct packages in main db
    db_client.execute(OSSZESITO_TABLE_INSERT_FROM_CSOMAG)

    # selecting users from disting packages
    columns, result = db_client.select(OSSZESITO_TABLE_SELECT_DISTINCT_USERS)

    # getting users
    users = []
    for row in result:
        for cell in row:
            users.append(cell)

    # checking packages by Octopus 8
    columns, result = db_client.select(OSSZESITO_TABLE_SELECT)
    for row in result:
        row_id = row[0]
        csomagszam = row[1]
        text_to_log("searching for package no. '" + csomagszam + "' in Octopus 8...")
        csomagszam_o8_lookup = o8_client.one_value_select(O8_SELECT_INFO_BY_CSOMAGSZAM, (csomagszam,))
        db_client.execute(OSSZESITO_UPDATE_O8_CONFIRM, (csomagszam_o8_lookup, row_id))

    # Adding date for found Octopus 8 packages
    columns, result = db_client.select(OSSZESITO_SELECT_CONFIRMED)
    for row in result:
        row_id = row[0]
        csomagszam = row[1]
        text_to_log("searching for CRDTI '" + csomagszam + "' in Octopus 8...")
        csomagszam_o8_crdti = o8_client.one_value_select(O8_SELECT_CRDTI_BY_CSOMAGSZAM, (csomagszam,))
        db_client.execute(OSSZESITO_UPDATE_O8_CRDTI, (csomagszam_o8_crdti, row_id))

    # creating worksheets
    if users:
        worksheets = []

        # Summary
        text_to_log("creating summary...")
        columns, results = db_client.select(XLSX_OSSZESITO_SELECT)
        worksheet = funct.xlsx_handle.worksheet(
            name = "Összesítő",
            header = columns,
            data = results
        )
        worksheets.append(worksheet)

        # Users
        for user in users:
            columns, results = db_client.select_with_arg(OSSZESITO_SELECT_BY_USER, (user,))
            # fetching username for usercode
            username = o8_client.one_value_select(query = USER_SELECT_BY_USERCODE, insert = int(user))
            text_to_log("creating worksheet for user: " + username)

            worksheet = funct.xlsx_handle.worksheet(
                name = username,
                header = columns,
                data = results
            )
            worksheets.append(worksheet)

        # creating workbook
        if worksheets:
            workbook = funct.xlsx_handle.workbook(
                name = "Csomagolás kimutatás",
                content = worksheets
            )

            # Exports to xlsx
            xlsx_path = workbook.xlsx_create(file_path = config_path.temp_path, file_name = current_datetime_to_string() + "_" + workbook.name)
            xlsx_name = funct.file_handle.get_filename_from_path(xlsx_path)
            ftp_client.upload(xlsx_path, "kimutatas", xlsx_name)

    # closing connections
    o8_client.close()
    db_client.close()

    ftp_client.delete_all_db_files(FTP_INFO["directory"])

if __name__ == "__main__":
    main()
