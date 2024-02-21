import config_path
import os
from funct.log import text_to_log
from funct.sqlite_handle import Connection as sqlite_connection
from funct.db_config import csomag_table_create, osszesito_table_create
import funct.file_handle

def main():
    db_client = sqlite_connection()
    db_client.execute(csomag_table_create)
    db_client.execute(osszesito_table_create)
    files = funct.file_handle.ls_with_path(os.path.join(config_path.path, config_path.logs_subpath))
    

if __name__ == "__main__":
    main()