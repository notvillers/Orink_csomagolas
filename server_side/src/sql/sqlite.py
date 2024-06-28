'''queries for the sqlite database'''

CSOMAG_TABLE_CREATE: str = """


    CREATE TABLE IF NOT EXISTS csomag (
        id INTEGER NOT NULL,
        csomagszam TEXT NOT NULL,
        user TEXT NOT NULL,
        hostname TEXT NOT NULL,
        crdti DATETIME NOT NULL,
        unique (id, csomagszam, user, hostname, crdti)
    );
"""

CSOMAG_TABLE_INSERT: str = """
    INSERT or IGNORE INTO csomag (
        id,
        csomagszam,
        user,
        hostname,
        crdti
    ) VALUES (?, ?, ?, ?, ?);
"""

CSOMAG_TABLE_DELETE: str = """
    DELETE FROM csomag WHERE csomagszam = ?;
"""

CSOMAG_TABLE_SELECT_ALL: str = """
    SELECT * FROM csomag;
"""

OSSZESITO_TABLE_CREATE: str = """
    CREATE TABLE IF NOT EXISTS osszesito (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        csomagszam TEXT NOT NULL,
        user TEXT NOT NULL,
        hostname TEXT NOT NULL,
        crdti DATETIME NOT NULL,
        o8_date DATETIME
    );
"""

OSSZESITO_TABLE_INSERT_FROM_CSOMAG: str = """
    INSERT or IGNORE INTO osszesito (csomagszam, user, hostname, crdti, o8_date)
    SELECT DISTINCT
        csomag.csomagszam csomagszam,
        (SELECT cs.user FROM csomag cs WHERE cs.csomagszam = csomag.csomagszam ORDER by cs.crdti ASC LIMIT 1) user,
        (SELECT cs.hostname FROM csomag cs WHERE cs.csomagszam = csomag.csomagszam ORDER by cs.crdti ASC LIMIT 1) hostname,
        (SELECT cs.crdti FROM csomag cs WHERE cs.csomagszam = csomag.csomagszam ORDER by cs.crdti ASC LIMIT 1) crdti,
        null o8_date
    FROM
        csomag
    WHERE
        NOT EXISTS (SELECT * FROM osszesito WHERE osszesito.csomagszam = csomag.csomagszam)
    ;
"""

OSSZESITO_SELECT_CSOMAGSZAM_WITHOUT_O8DATE: str = """
    SELECT csomagszam FROM osszesito WHERE o8_date IS NULL;
"""

OSSZESITO_UPDATE_CRDTI: str = """
    UPDATE osszesito SET o8_date = ? WHERE csomagszam = ?;
"""

USER_CREATE: str = """
    CREATE TABLE IF NOT EXISTS user (
        usercode INTEGER PRIMARY KEY,
        username TEXT NOT NULL
    );
"""

USER_INSERT: str = """
    INSERT or IGNORE INTO user (usercode, username) VALUES (?, ?);
"""

USER_SELECT: str = """
    SELECT * FROM user;
"""

XLSX_OSSZESITO_SELECT: str = """
    SELECT DISTINCT
        strftime('%Y.%m.%d', osszesito.o8_date) as 'Dátum',
        user.username as 'Felhasználó',
        (
            SELECT count(*) 
            FROM osszesito as osszesito_inner
            WHERE
                osszesito_inner.user = osszesito.user
                and osszesito_inner.o8_date is not NULL
                and strftime('%Y.%m.%d', osszesito.o8_date) = strftime('%Y.%m.%d', osszesito_inner.o8_date)
        ) as 'Ellenőrzött csomagok száma'
    FROM
        osszesito LEFT JOIN user ON osszesito.user = user.usercode
    WHERE
        osszesito.o8_date is not NULL
    order by strftime('%Y.%m.%d', osszesito.o8_date) DESC
    ;
"""

SELECT_USERS_WITH_CSOMAG: str = """
    select distinct user from csomag;
"""

SELECT_USERNAME_FOR_USERCODE: str = """
    select username from user where usercode = ?;
"""

SELECT_CSOMAG_FOR_USER: str = """
    select * from osszesito where user = ?;
"""
