'''queries for the o8 database'''

SELECT_CRDTI_BY_CSOMAGSZAM = """
    declare @csomagszam varchar(max) = ?

    select
        CASE
            WHEN @csomagszam LIKE '[%]%' then (select convert(varchar, CRDTI, 120) from WCSOMAG with (nolock) where CSOMAGSZAM like SUBSTRING(@csomagszam, 9, 14) + '%')
            else (select convert(varchar, CRDTI, 120) from WCSOMAG with (nolock) where CSOMAGSZAM = @csomagszam)
        end
    ;
"""

SELECT_USERS = """
    select USERCODE, USERNAME from USERS with (nolock) where USERACTIVE = 1
"""
