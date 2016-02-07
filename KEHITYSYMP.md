# Lokaalin ajoympäristön (kehitysympäristön) pystyttäminen:

## Versionhallinta

> Githubista kloonataan Team-Papukaanin repositorio omalle koneelle

> Linkki: [Team-Papukaani](https://github.com/Team-Papukaani/papukaani.git "jotain....")

## Ajoympäristön pystyttäminen

> Ohjeet ajoympäristön pystyttämiseen löytyvät Readme.md Asennusdokumentaatiosta

## Ajoympäristön käynnistäminen

* Järjestelmän ajamista varten aktivoidaan virtuaaliympäristö komennolla:

> *source pelikaijaenv/bin/activate*

* Paikallinen ympäristö käynnistetään komennolla:

> *python3 manage.py runserver*

* Kirjautumisen saa pois päältä lisäämällä edellisen komennon loppuun parametri –skipauth

> *python3 manage.py runserver –skipauth*

* Avataan selaimella

> *localhost:8000/papukaani/*

> Täällä voidaan katsoa, että tehdyt muutokset toimivat halutulla tavalla

## Jenkins

> Linkki: [Jenkins](http://fmnh-ws-test.it.helsinki.fi/jenkins/job/Papukaanitestit/ "Jenkins")

> Jenkins ajaa testit Papukaanitestit-jobissa, jonka jälkeen deployataan BuildApp-jobilla staging-palvelimelle. Palvelin kuitenkin joskus lakkaa toimimasta ja se pitää käynnistää uudelleen systemctl restart papukaani -komennolla staging-palvelimella.

## Testit

* Testien ajaminen tapahtuu komennolla:

> *./manage.py test -v 3*

* Jos halutaan nähdä selaintestit, loppuun lisätään parametri *–visible*

> *./manage.py test -v 3 --visible*
