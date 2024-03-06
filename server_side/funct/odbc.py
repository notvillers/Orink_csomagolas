'''odbc'''

import pyodbc

def get_driver():
    '''returns the driver name'''
    drivers = pyodbc.drivers()
    for driver in drivers:
        if driver.startswith('ODBC Driver ') and driver.endswith(' for SQL Server'):
            return driver.replace('ODBC Driver ', '').replace(' for SQL Server', '')
    return None