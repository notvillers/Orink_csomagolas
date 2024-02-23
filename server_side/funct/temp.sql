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