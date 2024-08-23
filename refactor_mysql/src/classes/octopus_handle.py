'''mssql db connection'''

from sys import exit as sys_exit
import os
from time import sleep
from ping3 import ping
import pyodbc
from villog import Logger

class MsSQLClient:
    '''mssql client class'''

    def __init__(self,
        server: str,
        database: str,
        username: str,
        password: str,
        is_trusted: bool = True,
        logger: Logger = None
    ) -> None:
        self.server: str = server
        self.database: str = database
        self.logger: Logger = logger
        self.connection: pyodbc.Connection = self.__connect(username, password, is_trusted)
        self.cursor: pyodbc.Connection.cursor = self.connection.cursor()

    def __str__(self) -> str:
        return f"{self.server}@{self.database}"

    def __log(self, content: str) -> None:
        '''log content'''
        if self.logger:
            self.logger.log(content)
        else:
            print(content)

    def __ping(self, attempt: int = 5, wait: int = 10) -> bool:
        '''ping the server'''
        if attempt != 0:
            response_time: float = ping(self.server)
            if response_time or response_time == 0:
                self.__log(f"{self.server} reached")
                return True
            else:
                self.__log(f"Can't reach {self.server}")
                attempt -= 1
                if attempt != 0:
                    self.__log(f"Retrying in {wait} seconds")
                    sleep(wait)
                    self.__ping(attempt, wait)
        self.__log(f"Can't reach {self.server}, no more attempts")
        return False

    def __get_driver(self) -> str:
        '''get the driver'''
        drivers = pyodbc.drivers()
        for driver in drivers:
            if driver.startswith("ODBC Driver ") and driver.endswith(" for SQL Server"):
                return driver.replace("ODBC Driver ", "").replace(" for SQL Server", "")
        return None

    def __connect(self, username: str, password: str, is_trusted: bool = True) -> pyodbc.Connection:
        if not self.__ping():
            sys_exit()
        odbc_driver: str = self.__get_driver()
        if not odbc_driver:
            self.__log("No ODBC driver found")
            sys_exit()
        connection_string: str = ""
        connection_string += 'DRIVER={ODBC Driver ' + odbc_driver
        connection_string += ' for SQL Server};SERVER=' + self.server
        connection_string += ';DATABASE=' + self.database
        connection_string += ';UID=' + username
        connection_string += ';PWD=' + password
        connection_string += ";TrustServerCertificate=" + ("yes;" if is_trusted else "no;")
        self.__log(f"Connecting to {self.server}@{self.database}")
        connection: pyodbc.Connection = pyodbc.connect(connection_string)
        self.__log(f"Connected to {self.server}@{self.database}")
        return connection

    def close(self) -> None:
        '''close connection'''
        self.cursor.close()
        self.connection.close()
        self.__log(f"Connection to {self.server} closed")

    def __execute(self, query: str, insert: list = None) -> tuple:
        '''execute query'''
        if insert is not None:
            self.cursor.execute(query, insert)
        else:
            self.cursor.execute(query)
        result = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return columns, result

    def select(self, query: str, insert: list = None) -> tuple:
        '''select query'''
        return self.__execute(query, insert)

    def one_value_select(self, query: str, insert: list = None) -> any:
        '''select one value'''
        _, result = self.select(query, insert)
        return result[0][0] if result else None

class Table:
    '''table class for Octopus 8'''
    def __init__(self,
        columns: list,
        rows: list[list],
    ):
        self.columns: list = columns
        self.rows: list[list] = rows

    def to_dict(self) -> dict:
        '''convert to dict'''
        return self.__dict__

    def __column_index(self, column_name: str) -> int:
        '''return column index'''
        for index, column in enumerate(self.columns):
            if column.lower() == column_name.lower():
                return index
        return None

    def return_column(self, column_name: str) -> list[str]:
        '''return column by name'''
        column_index: int = self.__column_index(column_name)
        if column_index is not None:
            return [row[column_index] for row in self.rows]
        return None

    def return_columns(self, column_names: list[str]) -> list[list]:
        '''return columns by names'''
        new_rows: list[list] = []
        for row in self.rows:
            new_row: list = []
            for column_name in column_names:
                column_index: int = self.__column_index(column_name)
                if column_index is not None:
                    new_row.append(row[column_index])
            new_rows.append(new_row)
        return new_rows

class Octopus:

    '''Octopus 8 class'''

    def __init__(self,
        login_data: dict = None,
        server: str = None,
        database: str = None,
        username: str = None,
        password: str = None,
        is_server_trusted: bool = True,
        do_logs: bool = True,
        logger: Logger = None,
        row_limit: int = None
    ) -> None:
        self.__do_logs: bool = do_logs
        if do_logs:
            if not logger:
                self.__logger: Logger = Logger(
                    file_path = os.path.join(os.getcwd(), "octopus.log"),
                )
            else:
                self.__logger: Logger = logger
        self.__client: MsSQLClient = MsSQLClient(
            server = self.__set_server_value(login_data, server, "server"),
            database = self.__set_server_value(login_data, database, "database"),
            username = self.__set_server_value(login_data, username, "username"),
            password = self.__set_server_value(login_data, password, "password"),
            is_trusted = is_server_trusted,
            logger = self.__logger
        )
        self.__row_limit: int = row_limit
        self.__tables: list[str] = self.__get_tables()

        for table in self.__tables:
            if table.lower() != "table":
                setattr(self,
                    f"get_table_{table.lower()}",
                    lambda
                        table = table,
                        raw_filter = "",
                        order_by = None,
                        **kfilter:
                        self.__get_table(
                            table,
                            raw_filter,
                            order_by,
                            **kfilter
                        )
                )

    def __str__(self) -> str:
        return str(self.__client)

    def __log(self, content):
        '''log content
        @param: content Content to log'''
        if self.__do_logs:
            self.__logger.log(content)
        else:
            print(content)

    def __check_key(self, dictionary: dict, key: str) -> bool:
        '''check key in dictionary
        @param: dictionary Dictionary
        @param: key Key'''
        if key in dictionary:
            return True
        return False

    def __set_server_value(self, login_data: dict, value: str, key: str) -> str:
        '''set server value
        @param: login_data Login data dictionary
        @param: value Value
        @param: key Key'''
        if self.__check_key(login_data, key):
            return login_data[key]
        if value:
            return value
        self.__log(f"No {key} found, exiting...")
        sys_exit(1)

    def __get_row_limit(self) -> str:
        '''get row limit to query'''
        if self.__row_limit and self.__row_limit > 0:
            return f" top {str(self.__row_limit)}"
        return ""
    
    def set_row_limit(self, row_limit: int) -> None:
        '''set row limit
        @param: row_limit Row limit'''
        self.__row_limit = row_limit

    def __get_tables(self) -> list[str]:
        '''get tables from database'''
        _, results = self.__client.select("select name from sys.tables")
        tables = [result[0] for result in results]
        if not tables:
            self.__log("No tables found")
            exit(1)
        return tables

    def __is_table(self, table: str) -> bool:
        '''check if table exists
        @param: table Table name'''
        for tbl in self.__tables:
            if tbl.lower() == table.lower():
                self.__log(f"Table '{table}' found")
                return True
        self.__log(f"Table '{table}' not found")
        return False

    def __kfilter_to_query(self, kfilter_item: list):
        '''convert kfilter item to query
        @param: kfilter_item Kwargs filter item'''
        if isinstance(kfilter_item[1], str):
            if kfilter_item[1].lower() in ("null", "is null"):
                return f"{kfilter_item[0]} is null"
            if kfilter_item[1].lower() in ("not null", "is not null"):
                return f"{kfilter_item[0]} is not null"
            return f"{kfilter_item[0]} = '{kfilter_item[1]}'"
        if isinstance(kfilter_item[1], int):
            return f"{kfilter_item[0]} = {kfilter_item[1]}"

    def __get_table(self, table, raw_filter: str = "", order_by: list[tuple] = None, **kfilter) -> Table:
        """
        Selects a table from the database with the given filters and order by clause

        Args:
            table (str): Table's name
            Raw_filter (str, optional): Raw filter string after where clause. Defaults to "". 
                Ex. "column like "%xyz%"
            order_by (list[tuple], optional): Order by clause. Defaults to None. 
                Ex. [("column_name_1", "ASC"), ("column_name_2", "DESC")]
            **kfilter: Kwargs filter after the where clause. Defaults to {}. 
                Ex. column_name_1 = "value_1", column_name_2 = 123

        Returns:
            Table | None: Table object or None if table not found or result is empty
        """
        if self.__is_table(table):
            query: str = f"select {self.__get_row_limit()} * from {table} with (nolock) where 1 = 1"
            if raw_filter:
                query += f" and {raw_filter}"
            if kfilter:
                for kfilter_item in kfilter.items():
                    query += f" and {self.__kfilter_to_query(kfilter_item)}"
            if order_by:
                query += " order by "
                for i, order in enumerate(order_by):
                    query += f"{order[0]} {order[1]}{'' if len(order_by)-1 == i else ', '} "
            self.__log(f"Executing: {(query)}")
            columns, result = self.__client.select(query)
            if result:
                return Table(columns, result)
        return None

    def get_table(self, table: str, raw_filter: str = "", order_by: list[tuple] = None, **kfilter) -> Table:
        """
        Selects a table from the database with the given filters and order by clause

        Args:
            table (str): Table's name
            Raw_filter (str, optional): Raw filter string after where clause. Defaults to "". 
                Ex. "column like "%xyz%"
            order_by (list[tuple], optional): Order by clause. Defaults to None. 
                Ex. [("column_name_1", "ASC"), ("column_name_2", "DESC")]
            **kfilter: Kwargs filter after the where clause. Defaults to {}. 
                Ex. column_name_1 = "value_1", column_name_2 = 123

        Returns:
            Table | None: Table object or None if table not found or result is empty
        """
        return self.__get_table(
            table = table,
            raw_filter = raw_filter,
            order_by = order_by,
            **kfilter
        )

    def custom_query(self, query: str, insert: tuple = None) -> tuple:
        """
        Selects a custom query from the database

        Arg:
            query (str): Query string

        Returns:
            tuple: Columns and result
        """
        if insert:
            return self.__client.select(query, insert)
        return self.__client.select(query)

    def custom_query_to_table(self, query: str, insert: tuple = None) -> Table:
        """
        Selects a custom query from the database and returns it as a Table object

        Arg:
            query (str): Query string

        Returns:
            Table: Table object
        """
        if insert:
            columns, result = self.custom_query(query, insert)
        else:
            columns, result = self.custom_query(query)
        if result:
            return Table(columns, result)
        return None

    def custom_query_only_columns(self, query: str, insert: tuple = None) -> list[str]:
        """
        Selects a custom query from the database and returns only the columns

        Arg:
            query (str): Query string

        Returns:
            list[str]: Columns
        """
        if insert:
            columns, _ = self.__client.select(query, insert)
            return columns
        columns, _ = self.__client.select(query)
        return columns

    def custom_query_only_values(self, query: str, insert: tuple = None) -> list[list]:
        """
        Selects a custom query from the database and returns only the values

        Arg:
            query (str): Query string

        Returns:
            list[list]: Values
        """
        if insert:
            _, result = self.__client.select(query, insert)
            return result
        _, result = self.__client.select(query)
        return result

    def close(self) -> None:
        '''close connection'''
        self.__client.close()
        self.__log(f"Connection to {self} closed")
