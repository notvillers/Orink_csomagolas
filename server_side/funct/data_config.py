'''Configuration datas'''

import os
import platform

IS_WINDOWS = (True if platform.system() == "Windows" else False)

WAIT_TIME = 30 # in second(s)
RETRY_ATTEMPT = 5 #

#Pyodbc
ODBC_DRIVER = "17"
if os.path.exists("odbc_ver_ps.py") and IS_WINDOWS:
    import odbc_ver_ps
    ODBC_DRIVER = str(odbc_ver_ps.verno)

O8_SELECT_USERNAME_BY_USERCODE = """
    SELECT username FROM users WHERE usercode = ?
    ;
"""

O8_SELECT_INFO_BY_CSOMAGSZAM = """
    SELECT CASE WHEN 'ORH1041398_1' IN (SELECT csomagszam FROM wcsomag) THEN 2 ELSE 1 END
    ;
"""
