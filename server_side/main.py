'''MAIN'''

import os
import config_path
from funct.sqlite_handle import Connection as sqlite_connection
import funct.db_config
import funct.file_handle
import funct.xlsx_handle
import funct.json_handle
import funct.octopus_handle
import funct.data_config

# sqlite query
CSOMAG_TABLE_CREATE = funct.db_config.CSOMAG_TABLE_CREATE
OSSZESITO_TABLE_CREATE = funct.db_config.OSSZESITO_TABLE_CREATE
CSOMAG_TABLE_SELECT = funct.db_config.CSOMAG_TABLE_SELECT
CSOMAG_TABLE_INSERT = funct.db_config.CSOMAG_TABLE_INSERT
OSSZESITO_TABLE_INSERT_FROM_CSOMAG = funct.db_config.OSSZESITO_TABLE_INSERT_FROM_CSOMAG
OSSZESITO_TABLE_SELECT_DISTINCT_USERS = funct.db_config.OSSZESITO_TABLE_SELECT_DISTINCT_USERS
OSSZESITO_SELECT_BY_USER = funct.db_config.OSSZESITO_SELECT_BY_USER

# octopus query
O8_SELECT_USERNAME_BY_USERCODE = funct.data_config.O8_SELECT_USERNAME_BY_USERCODE
O8_SELECT_INFO_BY_CSOMAGSZAM = funct.data_config.O8_SELECT_INFO_BY_CSOMAGSZAM

def main():
    '''main'''

    # Octopus 8 connection
    octopus_info = funct.json_handle.json_read(config_path.login_path)
    o8_client = funct.octopus_handle.Octopus8_sql(octopus_info)
    
    # main db connection
    db_client = sqlite_connection()
    db_client.execute(CSOMAG_TABLE_CREATE)
    db_client.execute(OSSZESITO_TABLE_CREATE)

    # getting .db files
    files = funct.file_handle.ls_with_path(os.path.join(config_path.path, config_path.LOGS_SUBPATH))

    # merging .db files
    for file in files:
        cache_db = sqlite_connection(file)
        columns, result = cache_db.select(CSOMAG_TABLE_SELECT)
        for row in result:
            db_client.insert(CSOMAG_TABLE_INSERT, (row[0], row[1], os.path.basename(file), row[2]))
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

    # creating worksheets
    if users:
        worksheets = []
        for user in users:
            columns, result = db_client.select_with_arg(OSSZESITO_SELECT_BY_USER, (user,))
            # fetchin username for usercode
            username = o8_client.one_value_select(query = O8_SELECT_USERNAME_BY_USERCODE, insert = int(user))

            worksheet = funct.xlsx_handle.worksheet(
                name = username,
                header = columns,
                data = result
            )
            worksheets.append(worksheet)

        # creating workbook
        if worksheets:
            workbook = funct.xlsx_handle.workbook(
                name = "Csomagolás kimutatás",
                content = worksheets
            )

            # Exports to xlsx
            workbook.xlsx_create(file_path = config_path.temp_path)


if __name__ == "__main__":
    main()
