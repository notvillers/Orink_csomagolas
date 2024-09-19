declare @csomagszam varchar(max) = ?

select
    CASE
        WHEN @csomagszam LIKE '[%]%' then (select convert(varchar, CRDTI, 120) from WCSOMAG with (nolock) where CSOMAGSZAM like SUBSTRING(@csomagszam, 9, 14) + '%')
        else (select convert(varchar, CRDTI, 120) from WCSOMAG with (nolock) where CSOMAGSZAM = @csomagszam)
    end
;