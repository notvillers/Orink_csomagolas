'''mssql db connection'''

import os
from time import sleep
from ping3 import ping
import pyodbc
from villog import Logger

class OctopusPythonException(Exception):
    '''Exception for Octopus 8 python module'''

class OctopusFunction:
    '''Octopus 8 function class'''

    def __init__(self,
        query: str,
        info: str|None = None
    ) -> None:
        self.query: str = query
        self.info: str|None = info

    def __str__(self) -> str:
        return self.query

class OctopusScalarValueFunctions:
    '''Octopus 8 scalar value functions class'''
    CIKKID_FROM_CIKKSZAM: OctopusFunction = OctopusFunction(
        query = "select c.CIKKID from CIKK c with (nolock) where c.CIKKSZAM = ?;",
        info = "? = cikkszam | Returns cikkid"
    )
    ELADHATO_KESZLET: OctopusFunction = OctopusFunction(
        query = "select dbo.F_GETCIKKKESZLET2(?, ?, 5, NULL, '3', NULL);",
        info = "? = cikkid, ? = raktarak | Returns eladhato keszlet"
    )
    F_GETCIKKKESZLET2: OctopusFunction = ELADHATO_KESZLET


class OctopusFunctions:
    '''Octopus 8 functions class'''
    scalar_value: OctopusScalarValueFunctions = OctopusScalarValueFunctions()


class MsSQLClient:
    '''mssql client class'''

    def __init__(self,
        server: str,
        database: str,
        username: str,
        password: str,
        is_trusted: bool = True,
        logger: Logger|None = None
    ) -> None:
        self.server: str = server
        self.database: str = database
        self.logger: Logger = logger
        self.connection: pyodbc.Connection = self.__connect(username, password, is_trusted)
        self.cursor: pyodbc.Connection.cursor = self.connection.cursor()

    def __str__(self) -> str:
        return f"{self.database}@{self.server}"

    def __log(self, content: str) -> None:
        '''log content'''
        if self.logger:
            self.logger.log(content)
        else:
            print(content)

    def __ping(self, attempt: int = 5, wait: int = 10) -> bool:
        '''ping the server'''
        if attempt != 0:
            response_time: float|None = ping(self.server)
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

    def __get_driver(self) -> str|None:
        '''get the driver'''
        drivers: list[str] = pyodbc.drivers()
        for driver in drivers:
            if driver.startswith("ODBC Driver ") and driver.endswith(" for SQL Server"):
                return driver.replace("ODBC Driver ", "").replace(" for SQL Server", "")
        if drivers:
            return drivers[0]
        return None

    def __connect(self, username: str, password: str, is_trusted: bool = True) -> pyodbc.Connection:
        '''connect to the server'''
        if not self.__ping():
            raise OctopusPythonException(f"{self.server} not reachable")
        odbc_driver: str = self.__get_driver()
        if not odbc_driver:
            self.__log("No ODBC driver found")
            raise OctopusPythonException("No ODBC driver found")
        connection_string: str = ""
        connection_string += 'DRIVER={ODBC Driver ' + odbc_driver
        connection_string += ' for SQL Server};SERVER=' + self.server
        connection_string += ';DATABASE=' + self.database
        connection_string += ';UID=' + username
        connection_string += ';PWD=' + password
        connection_string += ";TrustServerCertificate=" + ("yes" if is_trusted else "no") + ";"
        self.__log(f"Connecting to {self.database}@{self.server}")
        connection: pyodbc.Connection = pyodbc.connect(connection_string)
        self.__log(f"Connected to {self.database}@{self.server}")
        return connection

    def close(self) -> None:
        '''close connection'''
        self.cursor.close()
        self.connection.close()
        self.__log(f"Connection to {self.server} closed")

    def __execute(self, query: str, insert: list|None = None) -> None:
        '''execute query'''
        if insert is not None:
            self.cursor.execute(query, insert)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        self.__log(f"Executed.")

    def execute(self, query: str, insert: list|None = None) -> None:
        '''execute query'''
        self.__execute(query, insert)

    def __execute_with_result(self, query: str, insert: list|None = None) -> tuple|None:
        '''execute query'''
        if insert is not None:
            self.cursor.execute(query, insert)
        else:
            self.cursor.execute(query)
        result = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return columns, result

    def select(self, query: str, insert: list|None = None) -> tuple|None:
        '''select query'''
        return self.__execute_with_result(query, insert)

    def one_value_select(self, query: str, insert: list|None = None) -> str|int|None:
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

    def __column_index(self, column_name: str) -> int|None:
        '''return column index'''
        for index, column in enumerate(self.columns):
            if column.lower() == column_name.lower():
                return index
        return None

    def return_column(self, column_name: str) -> list[str]|None:
        '''return column by name'''
        column_index: int | None = self.__column_index(column_name)
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
        login_data: dict|None = None,
        server: str|None = None,
        database: str|None = None,
        username: str|None = None,
        password: str|None = None,
        is_server_trusted: bool = True,
        do_logs: bool = True,
        logger: Logger|None = None,
        row_limit: int|None = None,
        do_table_fetch: bool = True,
        allow_execute: bool = False
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
        self.__row_limit: int|None = row_limit
        self.__tables: list[str] = self.__get_tables()

        if do_table_fetch:
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

        self.__allow_execute: bool = allow_execute

    eladhato_keszlet_raktarak: list[str]|None = None
    __functions: OctopusFunctions = OctopusFunctions()

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
        raise OctopusPythonException(f"No '{key}' found")

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
            raise OctopusPythonException("No tables found")
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

    def __get_table(self, table, raw_filter: str = "", order_by: list[tuple]|None = None, **kfilter) -> Table:
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

    def get_table(self, table: str, raw_filter: str = "", order_by: list[tuple]|None = None, **kfilter) -> Table:
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

    def custom_query(self, query: str) -> tuple|None:
        """
        Selects a custom query from the database

        Arg:
            query (str): Query string

        Returns:
            tuple: Columns and result
        """
        return self.__client.select(query)

    def custom_query_to_table(self, query: str) -> Table:
        """
        Selects a custom query from the database and returns it as a Table object

        Arg:
            query (str): Query string

        Returns:
            Table: Table object
        """
        columns, result = self.custom_query(query)
        if result:
            return Table(columns, result)
        return None

    def custom_query_only_columns(self, query: str) -> list[str]|None:
        """
        Selects a custom query from the database and returns only the columns

        Arg:
            query (str): Query string

        Returns:
            list[str]: Columns
        """
        columns, _ = self.__client.select(query)
        return columns

    def custom_query_only_values(self, query: str) -> list[list]|None:
        """
        Selects a custom query from the database and returns only the values

        Arg:
            query (str): Query string

        Returns:
            list[list]: Values
        """
        _, result = self.__client.select(query)
        return result

    def __execute(self, query: str, insert: list|None = None) -> None:
        '''execute a query'''
        if self.__allow_execute:
            self.__client.execute(query, insert)
        else:
            raise OctopusPythonException("Execution is not allowed, set 'allow_execute' to True")

    def execute(self, query: str, insert: list|None = None) -> None:
        """
        Execute a query

        Args:
            query (str): Query string
            insert (list, optional): Insert values. Defaults to None.
        """
        self.__execute(query, insert)

    def __read_file(self, path: str, encoding: str = "utf-8-sig") -> str:
        '''read file content'''
        if not os.path.exists(path):
            raise OctopusPythonException(f"File not found: {path}")
        with open(path, "r", encoding = encoding) as file:
            return file.read()

    def __execute_file(self, path: str, encoding: str = "utf-8-sig") -> None:
        '''execute file content'''
        return self.custom_query(self.__read_file(path, encoding))

    def execute_file(self, path: str, encoding: str = "utf-8-sig") -> None:
        '''execute file content'''
        return self.__execute_file(path, encoding)
    
    def execute_file_to_table(self, path: str, encoding: str = "utf-8-sig") -> Table:
        '''execute file content to table'''
        return self.custom_query_to_table(self.__read_file(path, encoding))

    def get_cikkid_from_cikkszam(self, cikkszam: str) -> int|None:
        """
        Get cikkid from cikkszam

        Arg:
            cikkszam (str): Cikkszam

        Returns:
            int: Cikkid
        """
        query: str = self.__functions.scalar_value.CIKKID_FROM_CIKKSZAM.query
        value: int | None = self.__client.one_value_select(query, (cikkszam))
        return value if value else None

    def set_eladhato_raktarak(self, raktarak: list[str]) -> None:
        """
        Set the raktarak for eladhato keszlet

        Arg:
            raktarak (list[str]): Raktarak
        """
        self.eladhato_keszlet_raktarak = raktarak
        self.__log(f"Eladhato keszlet raktarak set to: {self.eladhato_keszlet_raktarak}")

    def __eladhato_keszlet_raktarak_to_str(self, separator: str = ";", raktarak: list[str]|None = None) -> str:
        '''convert eladhato keszlet raktarak to string'''
        if not raktarak and  not self.eladhato_keszlet_raktarak:
            raise OctopusPythonException("Üres az eladható raktárak listája")
        raktarak: list[str] = raktarak if raktarak else self.eladhato_keszlet_raktarak
        return separator.join([raktar for raktar in raktarak])

    def __get_eladhato_keszlet(self, cikkid: int|None = None, cikkszam: str|None = None, raktarak: list[str] = None) -> float|None:
        '''get eladhato keszlet'''
        f_cikkid: int|None = None
        if cikkid:
            f_cikkid = cikkid
        if cikkszam:
            f_cikkid = self.get_cikkid_from_cikkszam(cikkszam)
        if f_cikkid is None:
            return None
        if raktarak:
            raktarak_str: str = self.__eladhato_keszlet_raktarak_to_str(raktarak = raktarak)
        else:
            raktarak_str: str = self.__eladhato_keszlet_raktarak_to_str()
        if not f_cikkid or not raktarak_str:
            return None
        query: str = self.__functions.scalar_value.ELADHATO_KESZLET.query
        value: int = self.__client.one_value_select(query, (f_cikkid, raktarak_str))
        return float(value) if float(value) else 0

    def get_eladhato_keszlet(self, cikkid: int|None = None, cikkszam: str|None = None, raktarak: list[str]|None = None) -> float|None:
        """
        Get eladható készlet

        Arg:
            cikkid (int. optional): Cikkid
            cikkszam (str. optional): Cikkszam
            raktarak (list[str], optional): Raktarak

        Returns:
            int: Eladható készlet
        """
        keszlet: int = self.__get_eladhato_keszlet(cikkid, cikkszam, raktarak)
        return keszlet if keszlet else None
