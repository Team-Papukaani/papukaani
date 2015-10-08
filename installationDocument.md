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

Ohje on kirjoitettu Redhat-palvelimelle. Muissa Linux-jakeluissa mm. httpd ja apache-käyttäjä saattavat olla eri nimellä.

1. Cloonataan ohjelmatiedostot hakemistoon, jonne apache-käyttäjällä on luku- ja kirjoitusoikeudet ??
2. Luodaan Apache-konfiguraatiotiedosto /etc/httpd/conf.d/papukaani.conf seuraavalla sisällöllä:
>LoadModule proxy_module libexec/apache2/mod_proxy.so
><VirtualHost *:80>
>	ServerName papukaani.fqdn.osoite.tld
>
>	<Directory /polku/papukaani/papukaaniApp/static>
>           Options +Indexes
>	    AllowOverride none
>	    Require all granted
>	</Directory>
>	Alias /static /polku/papukaani/papukaaniApp/static
>	ProxyPass /static !
>	ProxyPass / http://localhost:8000/
>       ProxyPassReverse / http://localhost:8000/
></VirtualHost>

# WIP
