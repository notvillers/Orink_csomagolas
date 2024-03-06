'''Queries for the database'''

CSOMAG_TABLE_CREATE = """
    CREATE TABLE IF NOT EXISTS csomag
        (id INTEGER PRIMARY KEY, csomagszam TEXT, user TEXT, hostname TEXT, crdti DATETIME)
    ;
"""

CSOMAG_TABLE_INSERT = """
    INSERT or IGNORE INTO csomag
        (csomagszam, user, hostname, crdti)
        values 
        (?, ?, ?, ?)
"""

CSOMAG_TABLE_DELETE = """
    DELETE FROM csomag WHERE id = ?
    ;
"""

CSOMAG_TABLE_SELECT = """
    SELECT csomagszam, user, crdti FROM csomag ORDER BY id DESC
    ;
"""

CSOMAG_DISTINCT_SELECT = """
    SELECT DISTINCT csomagszam, id, user, hostname FROM csomag ORDER BY crdti ASC
    ;
"""

# # # # #

OSSZESITO_TABLE_CREATE = """
    CREATE TABLE IF NOT EXISTS osszesito
        (id INTEGER PRIMARY KEY, csomagszam TEXT, user TEXT, hostname TEXT, crdti DATETIME, o8_confirm INTEGER, o8_date DATETIME)
    ;
"""

OSSZESITO_TABLE_INSERT = """
    INSERT OR IGNORE INTO osszesito
        (csomagszam, user, hostname, crdti, o8_confirm)
        values
        (?, ?, ?, ?, 0)
;
"""

OSSZESITO_TABLE_INSERT_FROM_CSOMAG = """
    INSERT or IGNORE INTO osszesito (csomagszam, user, hostname, crdti, o8_confirm)
    SELECT DISTINCT
        csomag.csomagszam csomagszam,
        (SELECT cs.user FROM csomag cs WHERE cs.csomagszam = csomag.csomagszam ORDER by cs.crdti ASC LIMIT 1)  user,
        (SELECT cs.hostname FROM csomag cs WHERE cs.csomagszam = csomag.csomagszam ORDER by cs.crdti ASC LIMIT 1)  hostname,
        (SELECT cs.crdti FROM csomag cs WHERE cs.csomagszam = csomag.csomagszam ORDER by cs.crdti ASC LIMIT 1)  crdti,
        0 o8_confirm
    FROM 
        csomag
    WHERE 
        NOT EXISTS (SELECT * FROM osszesito WHERE osszesito.csomagszam = csomag.csomagszam)
    ; 
"""

OSSZESITO_TABLE_DELETE = """
    DELETE FROM osszesito WHERE id = ?
    ;
"""

OSSZESITO_TABLE_SELECT = """
    SELECT id as 'ID', csomagszam as 'Csomagszám', user as 'Rögzítő', crdti as 'Rögzítése dátuma' FROM osszesito
    ;
"""

OSSZESITO_TABLE_SELECT_DISTINCT_USERS = """
    SELECT DISTINCT user from osszesito
    ;
"""

OSSZESITO_SELECT_BY_USER = """
    SELECT id as 'ID', csomagszam as 'Csomagszám', replace(replace(hostname, '.db', ''), '_log', '') as 'Host', crdti as 'Rögzítés ideje'
    FROM osszesito 
    WHERE user = ?
    ;
"""

O8_SELECT_USERNAME_BY_USERCODE = """
    SELECT username FROM users WHERE usercode = ?
    ;
"""

O8_SELECT_INFO_BY_CSOMAGSZAM = """
    SELECT CASE WHEN 'ORH1041398_1' IN (SELECT csomagszam FROM wcsomag) THEN 2 ELSE 1 END
    ;
"""