'''main script'''

from datetime import datetime
from config.ConfigDroid import ConfigDroid
from src.classes.slave import Slave
from src.classes.sqlite_handle import SqliteHandle
from src.classes.json_handle import JsonHandle
from src.classes.ftp_handle import FTPHandle
from src.classes.mssql_handle import MssqlClient
from villog.writexcel import WorkSheet, WorkBook

def get_main_db_connection(droideka: ConfigDroid) -> SqliteHandle:
    '''get main db connection'''
    return SqliteHandle(droideka.get_db_path(), droideka.logger)

def try_to_create_tables(sqlite_main: SqliteHandle, slave: Slave) -> None:
    '''try to create tables'''
    sqlite_main.execute(slave.sqlite.csomag_create)
    sqlite_main.execute(slave.sqlite.osszesito_create)
    sqlite_main.execute(slave.sqlite.user_create)

def get_ftp_connection(droideka: ConfigDroid) -> FTPHandle:
    '''get ftp connection'''
    ftp_json = JsonHandle(droideka.get_ftp_path())
    return FTPHandle(
        hostname = ftp_json.content["hostname"],
        username = ftp_json.content["username"],
        password = ftp_json.content["password"],
        logger = droideka.logger
    )

def get_o8_connection(droideka: ConfigDroid) -> MssqlClient:
    '''get o8 connection'''
    o8_json = JsonHandle(droideka.get_o8_login_path())
    return MssqlClient(
        server = o8_json.content["server"],
        database = o8_json.content["database"],
        username = o8_json.content["username"],
        password = o8_json.content["password"],
        logger = droideka.logger
    )

def result_to_csv(result: list[list], path: str , encoding: str = "utf-8-sig") -> str:
    '''result to csv'''
    with open(path, "w", encoding = encoding) as file:
        for row in result:
            line = ','.join(str(item) for item in row)
            file.write(line + '\n')
    return path

def main(droideka: ConfigDroid) -> None:
    '''main function'''

    slave = Slave()

    # sqlite connection for main database
    sqlite_main = get_main_db_connection(droideka)
    try_to_create_tables(sqlite_main, slave)

    # read ftp.json
    ftp_json = JsonHandle(droideka.ftp_path)

    # ftp connection
    ftp = get_ftp_connection(droideka)
    ftp_dir: str = ftp_json.content["directory"]

    # check if there are files in the remote directory
    if ftp.list_files(ftp_dir):
        droideka.log(f"Files found in {ftp_dir}")
        ftp.download_files_with_extension(ftp_dir, droideka.get_log_path(), ".db")

        # list downloaded files
        files = slave.list_files_with_extension(droideka.get_log_path(), ".db")
        # insert into main database
        if files:
            for file in files:
                sqlite_log = SqliteHandle(file, droideka.logger)
                columns, results = sqlite_log.select(slave.sqlite.csomag_select_all)
                for result in results:
                    sqlite_main.execute(slave.sqlite.csomag_insert, result)
                sqlite_log.close()
            # create oszesito
            sqlite_main.execute(slave.sqlite.osszesito_insert_from_csomag)
    else:
        droideka.log(f"{ftp_dir} is empty")

    # select csomagszam without crdti
    columns, result = sqlite_main.select(slave.sqlite.osszesito_select_csomagszam_without_date)
    mssql = get_o8_connection(droideka)
    if result:
        for row in result:
            csomagszam: str = row[0]
            droideka.log(f"Searching Octopus 8 crdti for {csomagszam}")
            date: datetime = mssql.one_value_select(slave.o8.select_crdti_by_csomagszam, [csomagszam])
            if date:
                droideka.log(f"{str(date)}")
                sqlite_main.execute(slave.sqlite.osszesito_update_crdti, [date, csomagszam])
            else:
                droideka.log("Not found")

    # get users
    columns, result = mssql.select(slave.o8.select_users)
    if result:
        droideka.log("Updating users from o8")
        for row in result:
            sqlite_main.execute(slave.sqlite.user_insert, row)
    columns, result = sqlite_main.select(slave.sqlite.user_select)
    if result:
        droideka.log(
            f"user.csv created at {result_to_csv(result, droideka.user_csv_path)}"
        )

    # create xlsx
    # create summary
    columns, result = sqlite_main.select(slave.sqlite.xlsx_osszesito_select)
    if result:
        sheets: list = []
        sheets.append(
            WorkSheet(
                name = "Összesítő",
                header = columns,
                data = result
            )
        )
        # create separated sheets for user
        columns, result = sqlite_main.select(slave.sqlite.select_user_with_csomag)
        if result:
            for row in result:
                columns, result = sqlite_main.select(slave.sqlite.select_username_for_usercode, [row[0]])
                username = result[0][0]
                columns, result = sqlite_main.select(slave.sqlite.select_csomag_for_user, [row[0]])
                sheets.append(
                    WorkSheet(
                        name = username,
                        header = columns,
                        data = result
                    )
                )
        # create xlsx
        xlsx: WorkBook = WorkBook(
            name = "Csomagolás kimutatás",
            content = sheets
        )
        xlsx_path: str = xlsx.xlsx_create(file_path = droideka.result_path)
        xlsx_name: str = xlsx.name if xlsx.name.lower().endswith(".xlsx") else f"{xlsx.name}.xlsx"
        ftp.upload(xlsx_path, "kimutatas", xlsx_name)
    sqlite_main.close()
    mssql.close()
