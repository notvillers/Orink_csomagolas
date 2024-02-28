# Configuration datas

import os
import platform

isWindows = (True if platform.system() == "Windows" else False)

wait_time = 30 # in second(s)
retry_attempt = 5 #

#Pyodbc
odbc_driver = "17"
if os.path.exists("odbc_ver_ps.py") and isWindows:
    import odbc_ver_ps
    odbc_driver = str(odbc_ver_ps.verno)

o8_select_username_by_usercode = """
    SELECT username FROM users WHERE usercode = ?
    ;
"""

o8_select_info_by_csomagszam = """
    SELECT CASE WHEN 'ORH1041398_1' IN (SELECT csomagszam FROM wcsomag) THEN 2 ELSE 2 END
    ;
"""
