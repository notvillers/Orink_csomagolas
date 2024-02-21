# Queries for the database

csomag_table_create = """
    CREATE TABLE IF NOT EXISTS csomag
        (id INTEGER PRIMARY KEY, csomagszam TEXT, user TEXT, hostname TEXT, crdti DATETIME)
    ;
"""

csomag_table_insert = """
    INSERT INTO csomag
        (csomagszam, user, hostname, crdti)
        values 
        (?, ?, ?, CURRENT_TIMESTAMP)
    ;
"""

csomag_table_delete = """
    DELETE FROM csomag WHERE csomag.id = ?
    ;
"""

csomag_table_select = """
    SELECT id as 'ID', csomagszam as 'Csomagszám', user as 'Rögzítő' FROM csomag ORDER BY id DESC
    ;
"""

csomag_table_update_by_id = """
    UPDATE csomag set csomagszam = ? where id = ?
    ;
"""