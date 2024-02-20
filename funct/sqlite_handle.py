from funct.log import text_to_log
import os
import sqlite3
import config_path

class connection:

    def __init__(self, name: str = config_path.db_path):
        self.name = name
        self.connection = sqlite3.connect(self.name, detect_types = sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()
        text_to_log(self.name + " connection created")

    def __str__(self):
        return self.name
    
    def select(self, query: str):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return columns, result
    
    def execute(self, query: str, values: str = None):
        if values == None:
            self.cursor.execute(query)
            self.connection.commit()
            return
        self.cursor.execute(query, (values,))
        self.connection.commit()

    def insert(self, inserter: str, insert: str):
        self.cursor.execute(inserter, insert)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
        text_to_log(self.name + " connection closed")