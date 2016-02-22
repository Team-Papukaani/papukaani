## 1 - Kehitysympäristön pystyttäminen

Nämä ohjeet on kirjoitettu Ubuntulle.

Aluksi asenna seuraavat packaget `sudo apt-get install`in avulla:

    build-essential
    python3-dev python-pip python3-pip python-virtualenv  
    phantomjs xvfb xserver-xephyr 
    apache2 libapache-mod-wsgi-py3  

Asenna Java JDK jos sinulla ei vielä ole sitä. Se onnistuu helpoiten seuraavasti:

Etsi ja lataa uusin JDK .tar.gz -hakemistona, tiedostona jonka nimi on muotoa `jdk-8u71-linux-x64.tar.gz`. Ekstraktoi se ja saat kansion jonka nimi on muotoa `jdk1.8.0_71`. Sitten lisää tiedoston `~/.bashrc` loppuun seuraavaa muotoa olevat rivit:

    export JAVA_HOME=~/Downloads/jdk1.8.0_71
    export PATH=${PATH}:${JAVA_HOME}/bin

Sitten asenna *Oracle Instant Client* ja *Instant Client SDK* seuraavasti. Lataa ne [täältä](http://www.oracle.com/technetwork/topics/linuxx86-64soft-092277.html). Pura arkistot (ne purkautuvat samaan kansioon). Sen jälkeen lisää tiedostoon `~/.bashrc` seuraavan malliset rivit:

    export ORACLE_HOME=~/Downloads/instantclient_12_1
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME

Ja tee seuraava:

    cd /opt/oracle/instantclient_12_1
    ln -s libclntsh.so.12.1 libclntsh.so
    ln -s libocci.so.12.1 libocci.so

Luo uusi hakemisto ja sen sisälle uusi python-virtualenv:
  
    mkdir ~/pelikaija
    cd ~/pelikaija
    virtualenv -p python3 pelikaijaenv

Kloonaa repositorio luomaasi hakemistoon:

    git clone https://github.com/Team-Papukaani/papukaani

Asenna ohjelman vaatimat kirjastot luomaasi virtualenviin seuraavasti:
  
    source pelikaijaenv/bin/activate
    cd ~/pelikaija/papukaani
    pip install -r requirements.txt

Varmista että kaikki asentuvat ja ei tapahdu virheitä.

Lisää tiedostoon `~/.bashrc` sovelluksen tarvitsemat tunnukset ja salasanat:

    export LAJISTORE_USER=xxxxxx
    export LAJISTORE_PASSWORD=xxxxxx
    export LAJISTORE_TEST=xxxxxx
    export LAJISTORE_TEST_PASSWORD=xxxxxx
    export LAJISTORE_UNIT_TEST=xxxxxx
    export LAJISTORE_UNIT_TEST_PASSWORD=xxxxxx
    export TIPUAPI_USER=xxxxxx
    export TIPUAPI_PASSWORD=xxxxxx
    export LAJIAUTH_USER=xxxxxx

Tee djangon tarvitsemat "tietokantamigraatiot":

    ./manage.py makemigrations
    ./manage.py migrate
  
Kokeile ajaa sovellus djangon testiserverillä tekemällä 

    ./manage.py runserver

Ja testaa että pystyt avaamaan sovelluksen selaimella.

Sitten aja kaikki testit tekemällä

    ./manage.py test -v 3

Varmista että kaikki testit menevät läpi. Jos ne menevät, olet nyt valmis aloittamaan papukaanin kehittämisen. 

Lisää tietoa testaamisesta on [papukaanin wikissä](https://github.com/Team-Papukaani/papukaani/wiki/Testaaminen).

## 2 - Apache

Papukaani deployataan Apachen kanssa. Mutta et tarvitse apachea papukaanin kehittämiseen ja testaamiseen -- Djangon `runserver` -testiserveri korvaa sen.

Toimi Apachen kanssa seuraavasti:

<!---
Säädä static kansio pelikaija/papukaani/papukaani/config/common.py ???
-->

Muokataan /etc/apache2/sites-available/000-default.conf -tiedostoa ja lisätään VirtualHostin sisään (vaihda käyttäjänimet ja salasanat):
```apache
Alias /static /home/KÄYTTÄJÄNIMI/pelikaija/papukaani/papukaaniApp/static
<Directory /home/KÄYTTÄJÄNIMI/pelikaija/papukaani/papukaaniApp/static>
	Require all granted
</Directory>
<Directory /home/KÄYTTÄJÄNIMI/pelikaija/papukaani>
	<Files wsgi.py>
		Require all granted
	</Files>
</Directory>

# Muuta nämä
SetEnv LAJISTORE_USER xxxxxx
SetEnv LAJISTORE_PASSWORD xxxxx
SetEnv LAJISTORE_TEST xxxxx
SetEnv LAJISTORE_TEST_PASSWORD xxxxx
SetEnv PAPUKAANI_SECRET_KEY xxx
SetEnv LAJISTORE_UNIT_TEST xxx
SetEnv LAJISTORE_UNIT_TEST_PASSWORD xxxxx
SetEnv TIPUAPI_USER xxxx
SetEnv TIPUAPI_PASSWORD xxxx
SetEnv LAJIAUTH_USER xxxx

WSGIDaemonProcess satelliitti python-path=/home/KÄYTTÄJÄNIMI/pelikaija:/home/KÄYTTÄJÄNIMI/pelikaija/pelikaijaenv/lib/python3.4/site-packages
WSGIProcessGroup satelliitti
WSGIScriptAlias / /home/KÄYTTÄJÄNIMI/pelikaija/papukaani/papukaani/wsgi.py
```
<!---
Salli apachen päästä tietokantatiedostoon???
	chmod 664 ~/pelikaija/papukaani/db.sqlite3
	sudo chown :www-data ~/pelikaija/papukaani/db.sqlite3
-->

Annetaan Apachelle suoritus ja muokkausoikeudet tiedostoihin
```sh
chmod +x ~
sudo chown -R :www-data ~/pelikaija
```

Käynnistetään Apache uudelleen
```sh
sudo service apache2 restart
```

