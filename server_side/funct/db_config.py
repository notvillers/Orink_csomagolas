# Queries for the database

csomag_table_create = """
    CREATE TABLE IF NOT EXISTS csomag
        (id INTEGER PRIMARY KEY, csomagszam TEXT, user TEXT, hostname TEXT, crdti DATETIME)
    ;
"""

csomag_table_insert = """
    INSERT or IGNORE INTO csomag
        (csomagszam, user, hostname, crdti)
        values 
        (?, ?, ?, ?)
"""

csomag_table_delete = """
    DELETE FROM csomag WHERE id = ?
    ;
"""

csomag_table_select = """
    SELECT csomagszam, user, crdti FROM csomag ORDER BY id DESC
    ;
"""

csomag_distinct_select = """
    SELECT DISTINCT csomagszam, id, user, hostname FROM csomag ORDER BY crdti ASC
    ;
"""

# # # # # 

osszesito_table_create = """
    CREATE TABLE IF NOT EXISTS osszesito
        (id INTEGER PRIMARY KEY, csomagszam TEXT, user TEXT, hostname TEXT, crdti DATETIME)
    ;
"""

osszesito_table_insert = """
    INSERT OR IGNORE INTO osszesito
        (csomagszam, user, hostname, crdti)
        values
        (?, ?, ?, ?)
;
"""

osszesito_table_insert_from_csomag = """
    INSERT or IGNORE INTO osszesito (csomagszam, user, hostname, crdti)
    SELECT DISTINCT
        csomag.csomagszam csomagszam,
        (SELECT cs.user FROM csomag cs WHERE cs.csomagszam = csomag.csomagszam ORDER by cs.crdti ASC LIMIT 1)  user,
        (SELECT cs.hostname FROM csomag cs WHERE cs.csomagszam = csomag.csomagszam ORDER by cs.crdti ASC LIMIT 1)  hostname,
        (SELECT cs.crdti FROM csomag cs WHERE cs.csomagszam = csomag.csomagszam ORDER by cs.crdti ASC LIMIT 1)  crdti
    FROM 
        csomag
    WHERE 
        NOT EXISTS (SELECT * FROM osszesito WHERE osszesito.csomagszam = csomag.csomagszam)
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