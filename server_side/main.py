import config_path
import os
from funct.log import text_to_log
from funct.sqlite_handle import Connection as sqlite_connection
import funct.db_config
import funct.file_handle
import funct.xlsx_handle

csomag_table_create = funct.db_config.csomag_table_create
osszesito_table_create = funct.db_config.osszesito_table_create
csomag_table_select = funct.db_config.csomag_table_select
csomag_table_insert = funct.db_config.csomag_table_insert
osszesito_table_insert_from_csomag = funct.db_config.osszesito_table_insert_from_csomag
osszesito_table_select_distinct_users = funct.db_config.osszesito_table_select_distinct_users
osszesito_select_by_user = funct.db_config.osszesito_select_by_user

def main():
    # main db connection
    db_client = sqlite_connection()
    db_client.execute(csomag_table_create)
    db_client.execute(osszesito_table_create)

    # getting .db files
    files = funct.file_handle.ls_with_path(os.path.join(config_path.path, config_path.logs_subpath))

    # merging .db files
    for file in files:
        cache_db = sqlite_connection(file)
        columns, result = cache_db.select(csomag_table_select)
        for row in result:
            db_client.insert(csomag_table_insert, (row[0], row[1], os.path.basename(file), row[2]))
        os.remove(file)

    # creating distinct packages in main db
    db_client.execute(osszesito_table_insert_from_csomag)

    # selecting users from disting packages
    columns, result = db_client.select(osszesito_table_select_distinct_users)

    # getting users
    users = []
    for row in result:
        for cell in row:
            users.append(cell)
    
    # creating worksheets
    if users:
        worksheets = []
        for user in users:
            columns, result = db_client.select_with_arg(osszesito_select_by_user, (user,))
            worksheet = funct.xlsx_handle.worksheet(
                name = user,
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
            workbook.xlsx_create()


if __name__ == "__main__":
    main()