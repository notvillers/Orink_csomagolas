'''Queries for the database'''

CSOMAG_TABLE_CREATE = """
    CREATE TABLE IF NOT EXISTS csomag
        (id INTEGER PRIMARY KEY, csomagszam TEXT, user TEXT, hostname TEXT, crdti DATETIME)
    ;
"""

CSOMAG_TABLE_INSERT = """
    INSERT INTO csomag
        (csomagszam, user, hostname, crdti)
        values 
        (?, ?, ?, CURRENT_TIMESTAMP)
    ;
"""

CSOMAG_TABLE_DELETE = """
    DELETE FROM csomag WHERE id = ?
    ;
"""

CSOMAG_TABLE_SELECT = """
    SELECT id as 'ID', csomagszam as 'Csomagszám', user as 'Rögzítő' 
    FROM csomag 
    WHERE csomagszam NOT LIKE '%_work_state_%'
    ORDER BY id DESC
    ;
"""

CSOMAG_TABLE_UPDATE_BY_ID = """
    UPDATE csomag set csomagszam = ? where id = ?
    ;
"""
