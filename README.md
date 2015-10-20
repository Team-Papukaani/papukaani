# papukaani

[![Build Status](http://fmnh-ws-test.it.helsinki.fi/jenkins/buildStatus/icon?job=Papukaanitestit)](http://fmnh-ws-test.it.helsinki.fi/jenkins/job/Papukaanitestit/)

[![Code Climate](https://codeclimate.com/github/Team-Papukaani/papukaani/badges/gpa.svg)](https://codeclimate.com/github/Team-Papukaani/papukaani)

[Papukaani staging](http://papukaani-test.luomus.fi/papukaani)

## Asennusdokumentaatio

### Ohjeen komennot on Ubuntu 14.04:lle. 

Asennetaan Python3.4 (valmiiksi Ubuntussa), Apache2.4, sek‰ libapache2-mod-wsgi:n ett‰ python-virtualenv:n Python3-versiot:
```sh
sudo apt-get install apache2 libapache2-mod-wsgi-py3 python-virtualenv
```

Luodaan hakemisto ohjelmalle k‰ytt‰j‰n kotihakemistoon
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

Asennetaan ohjelman vaatimukset virtualenviin requirements.txt-tiedostosta Pip:ll‰
```sh
source pelikaijaenv/bin/activate
cd ~/pelikaija/papukaani
pip install -r requirements.txt
```

<!---
S‰‰d‰ static kansio pelikaija/papukaani/papukaani/config/common.py ???
-->

Tehd‰‰n tietokantamigraatiot ja poistutaan virtualenvist‰
```sh
./manage.py migrate
deactivate
```

Muokataan /etc/apache2/sites-available/000-default.conf -tiedostoa ja lis‰t‰‰n VirtualHostin sis‰‰n:
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

# Muuta n‰m‰
SetEnv LAJISTORE_USER xxxxxx
SetEnv LAJISTORE_PASSWORD xxxxx
SetEnv LAJISTORE_TEST xxxxx
SetEnv LAJISTRORE_TEST_PASSWORD xxxxx
SetEnv PAPUKAANI_SECRET_KEY xxx

WSGIDaemonProcess satelliitti python-path=/home/iivo/pelikaija:/home/iivo/pelikaija/pelikaijaenv/lib/python3.4/site-packages
WSGIProcessGroup satelliitti
WSGIScriptAlias / /home/iivo/pelikaija/papukaani/papukaani/wsgi.py
```
<!---
Salli apachen p‰‰st‰ tietokantatiedostoon???
	chmod 664 ~/pelikaija/papukaani/db.sqlite3
	sudo chown :www-data ~/pelikaija/papukaani/db.sqlite3
-->

Annetaan Apachelle suoritus ja muokkausoikeudet tiedostoihin
```sh
chmod +x ~
sudo chown -R :www-data ~/pelikaija
```

K‰ynnistet‰‰n Apache uudelleen
```sh
sudo service apache2 restart
```