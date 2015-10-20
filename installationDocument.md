# Asennusdokumentaatio

Ohje on kirjotettu Ubuntu 14.04:lle. 

Asennetaan Python3.4 (valmiiksi Ubuntussa), Apache2.4, sekä libapache2-mod-wsgi:n että python-virtualenv:n Python3-versiot:
```sh
sudo apt-get install apache2 libapache2-mod-wsgi-py3 python-virtualenv
```

Luodaan hakemisto ohjelmalle käyttäjän kotihakemistoon
```sh
mkdir ~/pelikaija && cd ~/pelikaija
```

Luodaan Python3-version virtualenv
```sh
virtualenv -p python3 pelikaijaenv
```

Kloonataan ohjelma hakemistoon
```sh
git clone https://github.com/Team-Papukaani/papukaani.git
```

Asennetaan ohjelman vaatimukset virtualenviin requirements.txt-tiedostosta Pip:llä
```sh
source pelikaijaenv/bin/activate
cd papukaani
pip install -r requirements.txt
```

<!---
Säädä static kansio pelikaija/papukaani/papukaani/config/common.py ???
-->

Tehdään tietokantamigraatiot ja poistutaan virtualenvistä
```sh
./manage.py makemigrations
./manage.py migrate
deactivate
```

Muokataan /etc/apache2/sites-available/000-default.conf -tiedostoa ja lisätään VirtualHostin sisään:
```apache
Alias /static /home/iivo/pelikaija/papukaani/papukaaniApp/static
<Directory /home/iivo/pelikaija/papukaani/papukaaniApp/static>
	Require all granted
</Directory>
<Directory /home/iivo/pelikaija/papukaani>
	<Files wsgi.py>
		Require all granted
	</Files>
</Directory>
WSGIDaemonProcess satelliitti python-path=/home/iivo/pelikaija:/home/iivo/pelikaija/pelikaijaenv/lib/python3.4/site-packages
WSGIProcessGroup satelliitti
WSGIScriptAlias / /home/iivo/pelikaija/papukaani/papukaani/wsgi.py
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