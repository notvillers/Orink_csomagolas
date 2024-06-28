'''sqlite db class'''

import sqlite3
from villog import Logger

class SqliteHandle:
    '''sqlite db class'''

    def __init__(self, db_path: str, logger: Logger) -> None:
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.logger = logger
        self.log(f"Connected to {self.db_path}")

    def __str__(self) -> str:
        return self.db_path

    def log(self, content: str) -> None:
        '''log content'''
        if self.logger:
            self.logger.log(content)
        else:
            print(content)

    def select(self, query: str, arg: list = None) -> tuple:
        '''select query'''
        if not arg:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, arg)
        result = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return columns, result

    def execute(self, query: str, arg: list = None) -> None:
        '''execute query'''
        if not arg:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, arg)
        self.connection.commit()

    def close(self) -> None:
        '''close connection'''
        self.cursor.close()
        self.connection.close()
        self.log(f"Connection to {self.db_path} closed")
