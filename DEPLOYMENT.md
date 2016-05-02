#### Papukaanitestit

Ajetaan kaikki master-branchin testit, kun jotain pushataan masteriin. Testien mennessä läpi ajetaan myös BuildApp-job.

```
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv update
pyenv local 3.4.3
pip install -r requirements.txt
./manage.py makemigrations
./manage.py migrate
./manage.py test -v 3
```


#### BuildApp

Deployataan koodi master-branchista testipalvelimelle.

```
cd /home/satelliitti
source env/bin/activate
rm -rf /home/satelliitti/papukaani
git clone https://github.com/Team-Papukaani/papukaani/
cd papukaani
pip install -r requirements.txt
./manage.py makemigrations
./manage.py migrate
chmod 777 db.sqlite3
chmod 777 papukaani.log
cd ..
chmod 777 papukaani
sudo /usr/bin/systemctl restart papukaani.socket
```


#### Hulvaton-Hiirihaukka-RC

Ajetaan kaikki hulvaton-hiirihaukka-rc -branchin testit, kun jotain pushataan kyseiseen branchiin.

```
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv update
pyenv local 3.4.3
pip install -r requirements.txt
./manage.py makemigrations
./manage.py migrate
./manage.py test -v 3
```


#### Johan on hemmetti kun ei mene testit läpi

Käytännössä yksittäisten testien/testi-keissien onnistumisen tarkasteluun käytetty jobi. Esimerkiksi tässä tapauksessa on
ajettu kaikki TestNewsFrontendin testit jenkinsissä.

```
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv update
pyenv local 3.4.3
pip install -r requirements.txt
./manage.py makemigrations
./manage.py migrate
./manage.py test -v 3 papukaaniApp.tests.testNewsFrontend.TestNewsFrontend
```
