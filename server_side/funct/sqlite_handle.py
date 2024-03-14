'''Sqlite3 handler'''

import sqlite3
from funct.log import text_to_log
import config_path

# Connection class
class Connection:
    '''sqlite3 connection class'''

    def __init__(self, name: str = config_path.db_path):
        self.name = name
        self.connection = sqlite3.connect(self.name, detect_types = sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()
        text_to_log(self.name + " connection created")

    def __str__(self):
        return self.name
    
    # Select query
    def select(self, query: str):
        '''selects query'''

        self.cursor.execute(query)
        result = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return columns, result

    def select_with_arg(self, query: str, arg = None):
        '''selects with argument(s)'''

        if arg is None:
            return self.select(query)
        self.cursor.execute(query, arg)
        result = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        return columns, result
    
    # Executes query with value argument
    def execute(self, query: str, values = None):
        '''executes query with value(s)'''

        if values is None:
            self.cursor.execute(query)
            self.connection.commit()
            return
        self.cursor.execute(query, values)
        self.connection.commit()
        return

    # Inserts query with inserter
    def insert(self, inserter: str, insert: str):
        '''inserts query with inserter'''

        self.cursor.execute(inserter, insert)
        self.connection.commit()

    # Closes cursor and connection
    def close(self):
        '''closes connection
        1. cursor
        2. connection'''

        self.cursor.close()
        self.connection.close()
        text_to_log(self.name + " connection closed")

    # Checks for value
    def is_value_there(self, columns, results, column_name: str, search_val):
        '''
        columns: the columns of the query result
        results: rows of the query result
        column_name: name of the searchable column
        search_val: searchable value in the searchable column's rows
        '''
        index = None
        for i, column in enumerate(columns):
            if column == column_name:
                index = i
                break
        if index is not None:
            for result in results:
                if result[index] == search_val:
                    return True
        return False
