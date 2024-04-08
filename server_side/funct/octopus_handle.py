'''Handles the database'''

import sys
from time import sleep
from ping3 import ping
import pyodbc
import funct.data_config
import funct.json_handle
from funct.log import text_to_log
from funct.odbc import get_driver

# Class for the Octopus 8 SQL connection
class Octopus8_sql:
    '''creates an octopus8 sql connection class
    needs a db_info dict passed for __init__'''

    def __init__(self, db_info):
        self.server = db_info["server"]
        self.database = db_info["database"]
        self.connection, self.cursor = self.connect(db_info["server"], db_info["database"], db_info["username"], db_info["password"])

    def __str__(self):
        return self.server + "\\" + self.database

    # Pings the server
    def ping_srvr(self, server, retry_attempt = funct.data_config.RETRY_ATTEMPT):
        '''pings with retry'''

        if retry_attempt != 0:
            response_time = ping(server)
            if response_time:
                text_to_log(server + " reached")
                return True
            else:
                text_to_log("can't reach " + server + ", retry in " + str(funct.data_config.WAIT_TIME) + " second(s)")
                sleep(funct.data_config.WAIT_TIME)
                text_to_log("retry:")
                self.ping_srvr(server, retry_attempt - 1)
        text_to_log("can't reach " + server + ", no more attempts")
        return False
    
    # Creates the connection and the cursor
    def connect(self, server, database, username, password):
        '''connects to sql with odbc'''

        if not self.ping_srvr(server):
            sys.exit()
        driver_version = get_driver()
        if driver_version is None:
            text_to_log("odbc driver not found")
            sys.exit()
        connection_string = 'DRIVER={ODBC Driver '+ driver_version + ' for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        text_to_log("connected to " + server + "\\" + database)
        return connection, cursor
    
    # Closes the connection
    def close(self):
        '''closes connection
        1. cursor
        2. connection'''

        self.cursor.close()
        self.connection.close()
        text_to_log("connection to " + self.server + "\\" + self.database + " is now closed")

    # Executing query
    def execute(self, query: str, insert = None):
        '''executes query and return columns, results of result'''

        if query:
            if insert is not None:
                self.cursor.execute(query, insert)
            else:
                self.cursor.execute(query)
            print("executed query")
            result = self.cursor.fetchall()
            columns = [column[0] for column in self.cursor.description]
            # text_to_log("returned " + str(len(result)) + " lines with " + str(len(columns)) + (" columns" if len(columns) > 1 else " column"))
            return columns, result
        return False, False
    
    # Returning 1 value select
    def one_value_select(self, query: str, insert):
        '''return 1 value from select
        used for 1 return queries'''

        columns, result = self.execute(query = query, insert = insert)
        return result[0][0]