# Papukaani-dokumentaatio

<img src="https://github.com/Team-Papukaani/papukaani/blob/master/papukaaniApp/static/papukaaniApp/logo.png?raw=true" width="300">

## Yleisesti

Papukaani on lintujen satelliittiseurantojen tietojen hallinnointi- ja visualisointijärjestelmä. Järjestelmään on toteutettu kaksi käyttäjäryhmää: tutkijat ja maallikot. Maallikot näkevät julkisessa näkymässä julkiseksi asetetut linnut ja pisteet. Tutkijoilta vaaditaan kirjautuminen, jonka jälkeen tutkija voi hallita lintuja ja lähettimiä, lähettää seurantatiedostoja, valita julkiset pisteet sekä luoda upotettavia karttoja.

Tyypillinen workflow menee siten, että tutkija lähettää seurantatiedoston (upload) ja valitsee julkiset pisteet (choose). Formaatin tiedot on oltava syötettynä ennen lähetystä (formats). Jos lintua ei ole vielä luotu (individuals) tai lähetintä ei ole vielä kiinnitetty lintuun (devices), tutkija tekee ne lähetyksen jälkeen. Tutkija voi luoda iframen (public) ja upottaa sen asianmukaiselle sivulle, ellei jo tehty.

## Järjestelmän osat

### Valintanäkymä (papukaani/choose)

Valintanäkymässä voidaan määrittää, mitkä pisteet näytetään julkisena kaikille käyttäjille. Kaikkia pisteitä ei pidä näyttää julkisesti, koska pesäpaikat tulee piilottaa. Tieto pisteen julkisuudesta on tallennettuna LajiStoressa gatheringin publicity-kentässä. Valittavia pisteitä voi rajata aikavälin mukaan helpompaa työstöä varten. Reset-nappi palauttaa pisteet muutoksia edeltäneeseen tilaan. 

Kun lähetin valitaan, pisteet ladataan LajiStoresta ja kartan koko mukautuu siten, että kaikki pisteet näkyvät. 

Toisiaan lähellä olevat pisteet kootaan rypäiksi. Rypään pinta-ala riippuu kartan zoom-tasosta - mitä lähemmäksi zoomataan, sitä pienemmältä pinta-alalta rypäät muodostuvat. Numeroarvo x/y kertoo, että rypäässä on x julkista pistettä ja y pistettä yhteensä.

Yksittäisiä pisteitä ja rypäitä vaihdetaan julkisiksi tai piilotetuiksi kaksoisklikkaamalla. Muutokset tallentuvat vasta Tallenna-nappia painettaessa. 

Ryväs on 
- harmaa, jos kaikki sen sisältämät pisteet ovat piilotettuja.
- vihreä, jos kaikki sen sisältämät pisteet ovat julkisia. 
- keltainen, jos se sisältää sekä piilotettuja että julkisia pisteitä.

Jos pisteet ovat aivan päällekkäin, ryvästä painamalla avautuu spider-valikko, josta yksittäisiä pisteitä voi valita.

Yksittäisestä pisteestä saa lisätietoja viemällä hiiren sen päälle. Kun rypään päälle viedään hiiri, kartalle piirtyy sinisellä pinta-ala sen sisältämistä pisteistä.

Kehitysehdotus: linnun valinta lähettimen valinnan sijaan. 

### Latausnäkymä (papukaani/upload)

Latausnäkymässä voidaan lähettää CSV-muotoisia tiedostoja LajiStoreen. Tiedoston formaatti valitaan valikosta. Jos formaatissa on vain yhden lähettimen tiedot ilman lähetintunnusta, täytetään lähetintunnus erikseen.

Lähetyksen jälkeen tiedostoa voi esikatsella kartalla. Muutokset pisteiden näkyvyteen tehdään valintanäkymässä (choose).

### Julkinen näkymä (papukaani/public)

Tämä sivu on kaikkien nähtävillä!

Kun listasta valitaan lintu, sen julkiset pisteet haetaan LajiStoresta ja reitti piirtyy kartalle. Play-napista voi aloittaa animaation, jonka nopeutta voi säätää nopeusvalitsimella. Linnun reittiä voi kelata kuten videota sijaintisäätimellä.

Karttapohjaa voi vaihtaa oikean yläkulman valitsimella. Mittakaavajana näkyy vasemmassa alakulmassa. Play-napin vieressä sekä karttamerkkiä painamalla näkee pisteen aikaleiman. Kirjautuneella on mahdollisuus luoda iframe luontihetkellä valituista parametreistä. Navigaatiopalkki ei näy kirjautumattomille.

Kehitysehdotus: nyt iframen generointi vähän hassussa paikassa. Ehkä kannattaa keksiä joku nätimpi ratkaisu. Ehkä myös kirjautumattomat voisivat luoda iframeja.

### Formaatin luonti (papukaani/formats)

Formaatti määritellään täyttämällä lomake. Lomakkeen riviä vastaa sarake CSV-tiedostossa ja kuhunkin kenttään täytetään sarakkeen nimi. Lomakkeella osa kentistä on pakollisia (merkattu tähdellä) ja osa valinnaisia (ilman tähteä). Pakolliset kentät on löydyttävä tiedostosta, kuten longitudi ja latitudi. Formaatin nimi on vapaamuotoinen tekstikenttä, jolla käyttäjä tunnistaa formaatin valikoissa. 

Aikaleima, päivämäärä ja kellonaika on merkitty kahdella tähdellä. Tämä tarkoittaa, että joko aikaleima-kenttä tai päivämäärä ja kellonaika -kentät ovat pakollisia. Jos formaatissa on yhdessä sarakkeessa aikaleima, joka sisältää sekä päivämäärän että kellonajan, täytetään aikaleima-kenttä. Jos taas päivämäärä ja kellonaika ovat eri sarakkeissa, täytetään vain päivämäärä ja aikaleima -kentät.

Kustakin kentästä saa lisätietoja lomakenäkymässä kysymysmerkki-painikkeesta.

Formaatteja voi muokata kynä-painikkeesta ja poistaa roskakori-painikkeesta.

Formaatit tallennetaan paikalliseen tietokantaan (tuotannossa Oracle) ja niitä käytetään ainoastaan latausnäkymässä tiedostoa lähetettäessä. Formaatin muuttaminen lähetyksen jälkeen ei aiheuta muutoksia jo lähetettyihin tiedostoihin.

### Lintujen hallinta (papukaani/individuals)

Lintujen hallinnassa lintuja voi lisätä, muokata ja poistaa. Lintujen tiedot tallennetaan LajiStoreen. Poisto piilottaa linnun, varsinaisen poiston asemesta, asettamalla linnun tietoihin piilotustiedon. Linnun lisäämisvaiheessa syötetään linnun nimi ja laji. Kun lintu on tallennettu, voidaan syöttää rengastunnus. Laji-kentässä voi valita lajin joko alasvetovalikosta tai kirjoittamalla osan lajin nimestä. Lajitiedot haetaan Tipu-APIsta. Laji on valittava ladatusta listasta eikä uutta lajia voi lisätä suoraan Papukaanista. Linnun tietoihin tallentuu lajin ID-tieto, jotta voidaan helpommin hakea eri kieliversio.

### Lähetinten hallinta (papukaani/devices)

Lähettimien hallinnassa valitaan, mikä lähetin on kiinnitetty mihinkin lintuun milläkin ajanjaksolla. Uusia lähettimiä ei voi lisätä tästä näkymästä, vaan lähetin luodaan automaattisesti latausnäkymässä, kun tallennetaan uuden lähettimen tietoja sisältävä tiedosto.

Kun valikosta valitaan lähetin, nähdään lähettimen historia. Lähetin kiinnitetään lintuun valitsemalla lintu valikosta, syöttämällä kiinnitysaika ja painamalla Kiinnitä-painiketta. Vastaavasti lähetin irrotetaan linnusta syöttämällä irrotusaika ja painamalla Irroita-painiketta. Aikakenttiin voi syöttää ajan näppäilemällä tai valitsemalla sen avautuvasta ikkunasta. 

Lähetin voi olla kiinnitettynä vain yhdessä linnussa kerrallaan. Linnulla voi olla nolla tai useampi lähetin kerrallaan.

## Arkkitehtuuri

### Tunnukset

Piilotettavat tunnisteet määritetään ympäristömuuttujiin. Readme.md:n ohjeessa on kuvattu niiden määritys mod_wsgi:lle. 

Staging-palvelimen Gunicorniin ympäristömuuttujat määritetään /etc/systemd/system/papukaani.service -tiedostossa.

Jenkinsissä ne määritetään: etusivu > Manage Jenkins > Configure System > Environment Variables. 

Tietokantayhteys Oracleen määritetään papukaani/config -hakemiston development.py ja production.py -tiedostoissa.

### LajiStore

LajiStoren kutakin dokumenttityyppiä vastaa Python-malli. Malleille on toteutettu CRUD-toiminnallisuudet. LajiStorea käytetään LajiStore-servicen (LajiStoreAPI.py) kautta.

Lue lisää LajiStoresta: [https://bitbucket.org/luomus/lajistore-api](https://bitbucket.org/luomus/lajistore-api)

### TipuApi

TipuApi-service hakee TipuApista tiedot lajeista Species-luokan ilmentyminä.

### LajiAuth

LajiAuthin toimintalogiikka on seuraava:

1. Kirjautumissivulla (login.html) on linkit kirjautumispalveluihin. Linkkien hrefissä kulkee järjestelmän tunnus ja relatiivinen polku, jonne ohjataan kirjautumisen jälkeen
2. Luomus määrittää järjestelmän tunnusta vastaavan uudelleenohjausosoitteen. Tunnuksia on kaksi: yksi stagingiin ja toinen localhostiin osoittava
3. Käyttäjä tulee takaisin järjestelmän login-sivulle POST pyynnöllä tokenin kanssa, joka luetaan backendissa parametrista "token"
4. Tokenin oikeellisuus lähetetään backendissä laji-authille validoitavaksi POST'n bodyssä
  - POST https://login.laji.fi/validation/
  - Content-Type: application/json
  - Body: &lt;token&gt;
5. Jos validation vastaa 'true', tokenin sisältöön voi luottaa -- Muussa tapauksessa käyttäjää ei tule päästää sisälle
6. Tokenista parsitaan käyttäjän tiedot. Token on selväkielistä jsonia

Lue lisää LajiAuthista: [https://bitbucket.org/luomus/laji-auth](https://bitbucket.org/luomus/laji-auth)

Papukaani-spesifisti kun validointi onnistuu, sessioon tallennetaan käyttäjänimi (laji_auth.py). Kun kutsutaan metodia, jolla on @require_auth -dekoraattori (require_auth.py), tarkistetaan käyttäjän kirjautuminen ja epäonnistuessa ohjataan kirjautumissivulle.

Kehitysympäristössä kirjautumisen voi ottaa pois päältä käynnistämällä palvelimen --skipauth -parametrilla, esim. *python3 manage.py runserver --skipauth*

### Public

Public-näkymä (public_views.py) näyttää navigaatiovalikon ja iframen-luonnin jos käyttäjä on kirjautunut sisään. Näkymälle on erikseen sallittu sen käyttö iframessa.

Public-näkymään haetaan lintujen metatiedot lajijärjestykessä. Parametrisointi on toteutettu Javascriptillä (public.js init-funktio).
Kun lintu on valittu, sen pisteet ladataan Javascriptillä (deviceSorter.js) REST-rajapinnasta (rest_views.py). Rajapinta palauttaa kaikki julkiset pisteet LajiStoresta myös sisäänkirjautumattomille. 

### Upload

Upload-näkymä (upload_views.py) palauttaa GET-pyynnöllä formaattiparserit, joista käyttäjä voi valita tiedostonsa formaatin. POST-pyynnöllä käsitellään lähetetty tiedosto. Tiedosto tallennetaan sekä LajiStoreen että omaan tietokantaan (Oracle) FileStorage-modelina.

### Choose

Choose-näkymä (choose_views.py) palauttaa GET-pyynnöllä lähettimet, joista käyttäjä voi valita kyseisen lähettimen pisteet ladattavaksi. Kun lähetin on valittu, ladataan kaikki lähettimen pisteet. Pisteiden aikaväliä rajataan Javascriptillä (choose.js). POST-pyynnöllä näkymään vaihdetaan pisteiden julkisuutta ja tallennetaan LajiStoreen.

### Devices

Devices-näkymä (device_views.py) palauttaa GET-pyynnöllä lintujen ja lähettimien tiedot. Käyttölittymä hyödyntää Javascriptiä laitteen historiatietojen näyttämiseen. Devices.js:ssä tehdään Ajax-pyynnöt näkymän attach_to ja remove_from -metodeihin, joilla lähettimiä kiinnitetään ja poistetaan linnuista vastaavasti.

### Individuals

Individuals-näkymä (individual_views.py) palauttaa GET-pyynnöllä ei-poistettujen lintujen tiedot sekä lajilistan TipuApista. POST-pyynnöillä näkymä joko lisää, muokkaa tai poistaa (merkitsee poistetuksi) lintuja LajiStoresta. 

### Formats

Formats-näkymä (formats_views.py) on moniosainen. Erillisenä osana on formaattien listausosio, jossa näkee formaattien nimen ja voi poistaa sekä aloittaa muokkauksen (list_formats.html). Toinen osa on formaatin muokkausnäkymä (formats.html). Formaattien tiedot tallennetaan omaan tietokantaan (Oracle).

### Testit

Selaintestit voidaan ajaa siten, että selain on näkyvissä. Tällöin testi ajetaan --visible -parametrilla, esim. *python3 manage.py test --visible*, mutta tällöin vaaditaan, että koneelle on asennettu sekä Firefox että Xephyr (Ubuntulla esim. xserver-xephyr, Archilla esim. xorg-server-xephyr). 

Selaintesteissä on hyödynnetty Page Object Design Patternia (esimerkiksi https://justin.abrah.ms/python/selenium-page-object-pattern--the-key-to-maintainable-tests.html). Patternin tavoitteena on erottaa testilogiikka käyttöliittymästä.

### Jenkins

Jenkins ajaa testit Papukaanitestit-jobissa, jonka jälkeen deployataan BuildApp-jobilla staging-palvelimelle. Palvelin kuitenkin joskus lakkaa toimimasta ja se pitää käynnistää uudelleen *systemctl restart papukaani* -komennolla staging-palvelimella.

### Testien rinnakkaisajo

EI TOIMI! LajiStore sekoittaa testit, jos sitä muokataan samaan aikaan. Tälle pitäisi keksiä jokin ratkaisu (aika kriittistä). 

## TODO

### Toteuttamatta jääneet epicit

- Julkisen näkymän pisteisiin tutkijalla mahdollisuus kiinnittää uutisia (+ monikielisyys)
- RSS-feedi linnun liikkeistä ja uutisista
- Julkaistavien pisteiden granulariteetti (nyt lataa kaikki mahdolliset pisteet)
- Useiden lintujen samanaikainen katselu julkisessa näkymässä
- Yhden linnun katselu usealla eri aikavälillä julkisessa näkymässä (esim. kevät 2015 ja kevät 2014)
- Eri käyttäjätasot (admin, webmaster, tutkija)
- Lähettimien tilan hallinnointi (kiinnitetty, ei-kiinnitetty, korjattavana, yms.)
- Valintanäkymässä undo-painike edelliselle/edellisille teoille
- Julkisen näkymän esikatselu valintanäkymässä ennen tallennusta

### Toteutusvinkkejä

Useamman linnun pisteiden samanaikainen näyttäminen vaatii animaattorille (polylineAnimate.js/Animator) toiminnallisuuden useampien pistesarjojen säilyttämiseen ja hallinnointiin (omat PathIteratorit jokaiselle). Tämän jälkeen voitaneen käyttää samaa setIntervalia jokaisen polun samanaikaiseen piirtämiseen. Tietenkin on lisäksi toteutettava jonkinlainen monivalinta linnuille.

Uutiset on suhteellisen helppo toteuttaa, jos ne voidaan yksilöidä linnun tunnisteella ja aikaleimalla. Tällöin ne voidaan Publicissa lisätä kartalle animaation kautta sitä mukaa, kun animaatio saavuttaa uutisen aikaleiman ajan.

### Toteuttamatta jääneet parannukset

- Mahdollisuus ajaa pelkät yksikkötestit paikallisesti
- Leaflet >= 1.0.0 siirtyminen
- Lähetinten hallinnassa vanhan kiinnitystiedon poisto
- TestDevicesFrontendin omituisten LajiStore-erroreiden selvittely
- 3D/syvyysanimoitu lintumarker (kts. hosuaby/Leaflet.SmoothMarkerBouncing)
- Testisemaforin digitalisointi
- Deploymentin ei pitäisi tarvita testausympäristön muuttujia
- GUI:hin base-template, jossa sivuilla toistuvat elementit
- Placeholder ei näy lajin valinnassa lintujen hallinnassa
- Redirect-pattern individualsin luontiin, muokkaukseen ja poistoon
- KML-tiedoston lataaminen julkisesta näkymästä
- Valintanäkymän pitäisi varoittaa poistuessa sivulta, jos on tallentamattomia muutoksia
- Julkisessa näkymässä pitäisi näyttää latauspalkki ym. ladatessa pisteitä.
- Mahdollisuus uploadata esimerkkitiedosto ja yhdistää tiedostossa olevat sarakkeet parserin attribuuteiksi tyyliin GPSTime -> timestamp jne.
- Serverin restarttaus deployatessa
- HTTPS-yhteys kirjautumisen tueksi
- WWW-juuresta ohjaus /papukaaniin
- Formaatin muokkausnäkymässä epäonnistuneen validoinnin jälkeen syötteet häviää
- Lähettimen valinnassa voi tulla päällekkäisyyksiä, kiinnityksen muokkaus
- Mobiilissa play-slider toimii huonosti

## Tehtävänanto

Tutkija lähettää datan. Alkuperäisdata jää talteen ja siitä karsitaan julkiseen näkymään tulevat pisteet. Kategorioita voisi olla kolme: julkiset, piilotetut ja virheellisiksi oletetut. Käytännössä tutkija jättää pesimäajan pois julkisista. Uutisia voi lisätä eri kielillä, joita maallikko voi lukea kartalta sekä RSS-feedinä. Mahdollinen automaattinen pesän sijainnin salaaminen.

Webmanager luo karttalaatikon, johon tulee yksilön reitti tiettynä vuodenaikana (kuten Mikko 2015 kesä). Yksilölle ja lajille luodaan nettisivut. 

Halutaan useamman yksilön samanaikainen näyttö kartalla, jossa on dynaaminen liikkeen seuranta. Julkisen näkymän oltava selkeä. Kartta pitäisi olla mahdollisimman iso ja sen päällä mahdollisimman vähän krumeluureja.

Jos linnun sijainti ei muutu, päivitysnopeutta lasketaan. Minimi puolen päivän välein päivitys. Tutkijan on mahdollista säätää päivitysparametreja yksilökohtaisesti.

GPS-laitevalmistajat tarjoavat API-palveluita vaihtelevasti. Mikä on Movebank? Ecotonen käyttöliittymästä voi ladata tiedoston Excel-muodossa. Järjestelmän on osattava käsitellä useita formaatteja ja niitä pitää pystyä lisäämään helposti. Datan pituus ja kenttien määrä vaihtelee.

Pisteet tallennetaan HTTP-rajapinnalla (käyttää Basic Authenticationia) ulkoiseen tietokantaan, LajiStoreen. Samoja pisteitä ei tallenneta kahteen kertaan. Tieto pisteen julkisuudesta tallentuu myös LajiStoreen.

Lähettimien hallinnointi ja niiden kiinnitys lintuihin tapahtuu ohjelman omassa tietokannassa (tietotekniikkakeskuksen Oracle). Lähettimiä uusiokäytetään.

Upotettavan iframen luonti valmiilla parametreilla, jotka ovat näytettävät linnut sekä aikaväli. Luettelo lajeittain, josta linkit karttoihin.

Tunnistautuminen järjestelmään salasanoilla on tärkeää. Kirjautumisessa käytetään Haka-autentikaatiota (toteutettuna LajiAuth). Admin voisi rajoittaa käyttäjien käyttöoikeuksia lintukohtaisesti. 

Värimaailmassa tulee huomioida värisokeat.

Pisteiden hallintaan raportointinäkymä, joka kertoo mitä tiedostoja ladattu, milloin, onko jotain lataamatta, ja kun lataa uuden tiedoston, miten se ylikirjoittaa muita tiedostoja. Graafiseen esitykseen esimerkiksi x-akselilla aika ja y-akselilla kuinka monta pistettä LajiStoressa.

## Staging-palvelin

Papukaanin osoite on [http://papukaani-test.luomus.fi/papukaani](http://papukaani-test.luomus.fi/papukaani) 

**HUOM** Staging-palvelimelle saa SSH- ja Oracle-yhteyden ainoastaan yliopiston verkosta. HUPnet ja Eduroam eivät ole sellaisia. Yhdistä esim. Melkin kautta.

Papukaania ajetaan gunicorn-sovelluspalvelimella, jonka käynnistämisestä pitää huolta seuraavat systemd-skriptit:
/etc/systemd/system/papukaani.service
/etc/systemd/system/papukaani.socket
/etc/tmpfiles.d/papukaani.conf

Papukaania voi hallita siis systemd-komennolla 
systemctl (start|stop|...) papukaani.socket

Palvelimelle lisätään käyttäjiä adduser -komennolla. Lisäämällä käyttäjä hysudo -ryhmään, esim. /etc/group -tiedostossa, saa tarvittavat oikeudet hallintakomentoihin

Asennusdokumentaatio on kuvattu [Readme.md-dokumentissa](https://github.com/Team-Papukaani/papukaani/blob/master/README.md)
