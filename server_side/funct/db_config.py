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
    SELECT id as 'ID', csomagszam as 'Csomagszám', user as 'Rögzítő', crdti as 'Rögzítése dátuma', o8_confirm as 'O8 ellenőrzés' FROM osszesito
    where o8_date is null
    ;
"""

OSSZESITO_TABLE_SELECT_DISTINCT_USERS = """
    SELECT DISTINCT user from osszesito
    ;
"""

OSSZESITO_SELECT_BY_USER = """
    SELECT id as 'ID', csomagszam as 'Csomagszám', replace(replace(hostname, '.db', ''), '_log', '') as 'Host', crdti as 'Rögzítés ideje', 
        case o8_confirm 
            when 0 then 'Nem volt ellenőrzés' 
            when 1 then 'Nem létező csomagszám'
            when 2 then 'Létező csomagszám'
        end as 'O8 ellenőrzés',
        o8_date as 'O8 rögzítés dátuma'
    FROM osszesito 
    WHERE user = ?
    ;
"""

OSSZESITO_UPDATE_O8_CONFIRM = """
    UPDATE osszesito SET o8_confirm = ? WHERE id = ?
    ;
"""

OSSZESITO_UPDATE_O8_CRDTI = """
    UPDATE osszesito SET o8_date = ? WHERE id = ?
    ;
"""

OSSZESITO_SELECT_CONFIRMED = """
    SELECT id, csomagszam from osszesito WHERE o8_confirm = 2 and o8_date is null
    ;
"""

# # # # #
USER_TABLE_CREATE = """
    CREATE TABLE IF NOT EXISTS users
        (usercode INTEGER, username TEXT)
    ;
"""

USER_TABLE_INSERT = """
    INSERT or IGNORE INTO users
        (usercode, username)
        values
        (?, ?)
    ;
"""

USER_TABLE_DELETE_ALL = """
    DELETE FROM users WHERE 1 = 1
    ;
"""

USER_SELECT_BY_USERCODE = """
    SELECT username FROM users WHERE usercode = ?
    ;
"""

# O8

O8_SELECT_USERNAME_BY_USERCODE = """
    SELECT username FROM users with (nolock) WHERE usercode = ?
    ;
"""

O8_SELECT_INFO_BY_CSOMAGSZAM = """
    declare @csomagszam varchar(max) = ?

    select
        case
            when exists (
                select top 1
                    COUNT(*) db
                from
                    WCSOMAG wcs with (nolock)
                where
                    wcs.CSOMAGSZAM = @csomagszam
                    or (@csomagszam like '[%]%' and wcs.CSOMAGSZAM like SUBSTRING(@csomagszam, 9, 14) + '%')
                ) then 2
            else 1
        end
    ;
"""

O8_SELECT_CRDTI_BY_CSOMAGSZAM = """
    declare @csomagszam varchar(max) = ?

    select
        CASE
            WHEN @csomagszam LIKE '[%]%' then (select convert(varchar, CRDTI, 120) from WCSOMAG with (nolock) where CSOMAGSZAM like SUBSTRING(@csomagszam, 9, 14) + '%')
            else (select convert(varchar, CRDTI, 120) from WCSOMAG with (nolock) where CSOMAGSZAM = @csomagszam)
        end
    ;
"""

O8_SELECT_USERS_FOR_CSV = """
    SELECT usercode, username FROM users with (nolock) WHERE users.usertipus = 1 and users.useractive = 1
    ;
"""

XLSX_OSSZESITO_SELECT = """
SELECT DISTINCT
	strftime('%Y.%m.%d', osszesito.o8_date) as 'Dátum',
	users.username as 'Felhasználó',
	(
		SELECT count(*) 
		FROM osszesito as osszesito_inner
		WHERE
			osszesito_inner.user = osszesito.user
			and osszesito_inner.o8_confirm = 2
			and strftime('%Y.%m.%d', osszesito.o8_date) = strftime('%Y.%m.%d', osszesito_inner.o8_date)
	) as 'Ellenőrzött csomagok száma'
    FROM
        osszesito LEFT JOIN users ON osszesito.user = users.usercode
    WHERE
        osszesito.o8_confirm = 2
        and osszesito.o8_date is not NULL
    order by strftime('%Y.%m.%d', osszesito.o8_date) DESC
    ;
"""
