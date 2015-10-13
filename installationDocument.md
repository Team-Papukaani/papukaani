# Asennusdokumentaatio - KESKENERÄINEN

## Vaatimukset

### Tuotantoympäristö

- Python3
- pip
- Oracle Instant client
- Apache
- Gunicorn

### Testausympäristö

- PyVirtualDisplay
- XVFB

## Asennus

1. Asenna Red Hat
2. Käynnistä verkkokortti (laita autom. käynnistyväksi /etc/sysconfig/network-scripts/ifcfg-enp0s3)
3. Laita SSH päälle komennoilla service sshd start && chkconfig sshd on
4. Rekisteröi Red Hat: subscription-manager register --username <username> --password <password> --auto-attach
5. Asenna Apache: yum install httpd
6. Asenna Python3.4.3: 
	muokataan notify_only=0 tiedostossa /etc/yum/pluginconf.d/search-disabled-repos.conf
	yum install wget gcc
	wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tar.xz
	tar xf Python-3.* 
	cd Python-3.*
	./configure
	make
	make altinstall

Ohje on kirjoitettu Redhat-palvelimelle. Muissa Linux-jakeluissa mm. httpd ja apache-käyttäjä saattavat olla eri nimellä.

1. Asenna Python3.4.3, Apache, Gunicorn
2. Asenna virtualenv Python3:n pipillä esim.
	sudo /usr/local/bin/pip install --upgrade virtualenv
3. Luo käyttäjätilit ja SSH-avaimet
	sudo useradd papukaani
	sudo su -l papukaani
	ssh-keygen
	exit
4. Lisää julkinen avain Githubiin / Bitbuckettiin
5. Kirjaudu käyttäjälle ja kloonaa repositorio kotihakemistoon
	sudo su -l papukaani
	umask 077
	cd ~
	git clone OSOITE

5.5 Enviromentin tekeminen

6. Cloonataan ohjelmatiedostot hakemistoon, jonne apache-käyttäjällä on luku- ja kirjoitusoikeudet ??
7. Luodaan Apache-konfiguraatiotiedosto /etc/httpd/conf.d/papukaani.conf seuraavalla sisällöllä:
```apache
LoadModule proxy_module libexec/apache2/mod_proxy.so
<VirtualHost *:80>
	ServerName papukaani.fqdn.osoite.tld

	<Directory /home/papukaani/papukaaniApp/static>
	    Options +Indexes
	    AllowOverride none
	    Require all granted
	</Directory>
	Alias /static /home/papukaani/papukaaniApp/static
	ProxyPass /static !
	ProxyPass / http://localhost:8000/
	ProxyPassReverse / http://localhost:8000/
</VirtualHost>
```

8. Luodaan /etc/systemd/system/papukaani.service:
```apache
[Unit]
Description=Papukaani
Requires=papukaani.socket
After=network.targetro

[Service]
PIDFile=/run/papukaani/pid
User=satelliitti
Group=satelliitti
WorkingDirectory=/home/satelliitti/papukaani
ExecStart=/home/satelliitti/env/bin/gunicorn --pid /run/papukaani/pid papukaani.wsgi
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```
9. Luodaan /etc/systemd/system/papukaani.socket
```apache
[Unit]
Description=papukaani socket

[Socket]
ListenStream=/run/papukaani/socket
ListenStream=0.0.0.0:9000
ListenStream=[::]:8000

[Install]
WantedBy=sockets.target
```
10. Luodaan /etc/tmpfiles.d/papukaani.conf
```apache
d /run/papukaani 0755 satelliitti satelliitti -
```

???
Koska tuotannossa staattisia tiedostoja ei lähetetä sovelluspalvelimen kautta, ne tulee kerätä yhteen paikkaan djangon collectstatic-hallintakomennolla Apachea varten:
$ source env/bin/activate
$ cd papukaani
$ python manage.py collectstatic
???


Papukaania voi hallita systemd-komennolla systemctl
(start|stop|...) papukaani.socket

# WIP
