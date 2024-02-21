# Sqlite3 handler

from funct.log import text_to_log
import os
import sqlite3
import config_path

# Connection class
class Connection:

    def __init__(self, name: str = config_path.db_path):
        self.name = name
        self.connection = sqlite3.connect(self.name, detect_types = sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()
        text_to_log(self.name + " connection created")

    def __str__(self):
        return self.name
    
    # Select query
    def select(self, query: str):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return columns, result
    
    # Executes query with value argument
    def execute(self, query: str, values = None):
        if values == None:
            self.cursor.execute(query)
            self.connection.commit()
            return
        self.cursor.execute(query, (values,))
        self.connection.commit()
        return 

    # Inserts query with inserter
    def insert(self, inserter: str, insert: str):
        self.cursor.execute(inserter, insert)
        self.connection.commit()

    # Closes cursor and connection
    def close(self):
        self.cursor.close()
        self.connection.close()
        text_to_log(self.name + " connection closed")

    # Checks for value
    '''
    columns: the columns of the query result
    results: rows of the query result
    column_name: name of the searchable column
    search_val: searchable value in the searchable column's rows
    '''
    def is_value_there(self, columns, results, column_name: str, search_val):
        index = None
        for i in range(len(columns)):
            if columns[i] == column_name:
                index = i
                break
        if index != None:
            for result in results:
                if result[index] == search_val:
                    return True
        return False