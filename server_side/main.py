import config_path
import os
from funct.log import text_to_log
from funct.sqlite_handle import Connection as sqlite_connection
from funct.db_config import csomag_table_create, osszesito_table_create, csomag_table_select, csomag_table_insert, osszesito_table_insert_from_csomag
import funct.file_handle

def main():
    db_client = sqlite_connection()
    db_client.execute(csomag_table_create)
    db_client.execute(osszesito_table_create)
    files = funct.file_handle.ls_with_path(os.path.join(config_path.path, config_path.logs_subpath))
    for file in files:
        cache_db = sqlite_connection(file)
        columns, result = cache_db.select(csomag_table_select)
        for row in result:
            db_client.insert(csomag_table_insert, (row[0], row[1], os.path.basename(file), row[2]))
        os.remove(file)
    db_client.execute(osszesito_table_insert_from_csomag)

if __name__ == "__main__":
    main()