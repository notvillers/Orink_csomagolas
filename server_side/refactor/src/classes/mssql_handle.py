'''mssql db connection'''

from sys import exit
from time import sleep
from ping3 import ping
import pyodbc
from villog import Logger

class MssqlClient:
    '''mssql client class'''

    def __init__(self, server: str, database: str, username: str, password: str, is_trusted: bool = True,logger = None) -> None:
        self.server: str = server
        self.database: str = database
        self.logger: Logger = logger
        self.connection = self.__connect(username, password, is_trusted)
        self.cursor = self.connection.cursor()

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
            exit()
        odbc_driver: str = self.__get_driver()
        if not odbc_driver:
            self.__log("No ODBC driver found")
            exit()
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
        columns, result = self.select(query, insert)
        return result[0][0] if result else None