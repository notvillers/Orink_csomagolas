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
"""

csomag_table_delete = """
    DELETE FROM csomag WHERE id = ?
    ;
"""

csomag_table_select = """
    SELECT id as 'ID', csomagszam as 'Csomagszám', user as 'Rögzítő' FROM csomag ORDER BY id DESC
    ;
"""

csomag_distinct_select = """
    SELECT DISTINCT csomagszam, id, user, hostname FROM csomag ORDER BY crdti ASC
    ;
"""

# # # # # 

osszesito_table_create = """
    CREATE TABLE IF NOT EXISTS osszesito
        (csomagszam TEXT, id INTEGER PRIMARY KEY, user TEXT, hostname TEXT, crdti DATETIME)
    ;
"""

osszesito_table_insert = """
    INSERT OR IGNORE INTO osszesito
        (csomagszam, user, hostname, crdti)
        values
        (?, ?, ?, CURRENT_TIMESTAMP)
;
"""

osszesito_table_delete = """
    DELETE FROM osszesito WHERE id = ?
    ;
"""

osszesito_table_select = """
    SELECT id as 'ID', csomagszam as 'Csomagszám', user as 'Rögzítő', crdti as 'Rögzítése dátuma' FROM osszesito
    ;
"""