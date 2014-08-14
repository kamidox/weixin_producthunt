weixin_producthunt
==================

1. Populate products from www.producthunt.com to weixin.
2. Automatically push the product list to user who follow @producthunt on weixin

environment setup
==================
1. run envsetup.sh to install software
    $ chmod +x ./envsetup.sh
    $ ./envsetup.sh

2. install Flask
    $ sudo pip install Flask

3. create database and tables
    $ mysql -uroot -p
    mysql> CREATE DATABASE producthunt
    mysql> source ../db/mysql.sql

4. deply by using Flask + uwsgi + nginx
=======================================
    4.1. config uwsgi
        4.1.1 save following config in "/etc/uwsgi/app-available/producthunt.xml"
        <uwsgi>
            <plugins>python</plugins>
            <master>true</master>
            <processes>1</processes>
            <vacuum>true</vacuum>
            <chmod-socket>666</chmod-socket>
            <socket>/tmp/uwsgi.producthunt.sock</socket>
            <uid>www-data</uid>
            <gid>www-data</gid>
            <pythonpath>/var/www/producthunt</pythonpath>
            <module>app</module>
            <callable>app</callable>
        </uwsgi>

        4.1.2 enable uwsgi app
        $ cd /etc/uwsgi/app-enabled
        $ sudo ln -s ../app-available/producthunt.xml .

    4.2. config nginx
        4.2.1 save following config in "/etc/nginx/sites-available/producthunt"
        server {
          listen 80;
          server_name 127.0.0.1;

          location / {
            include uwsgi_params;
            uwsgi_pass unix://tmp/uwsgi.producthunt.sock;
          }
        }

        4.2.2 remove the default config:
        $ sudo rm /etc/nginx/sites-enabled/default

        4.2.3 enable producthunt site
        $ cd /etc/nginx/sites-enabled
        $ sudo ln -s ../sites-available/producthunt .

    4.3. deply producthunt app
        $ sudo mkdir -p /var/www/
        $ sudo cp -R /path/to/prj/weixin /var/www/
        $ sudo mv /var/www/weixin /var/www/producthunt
        $ sudo chown -R www-data:www-data /var/www/producthunt

    4.4. start service
        $ sudo service uwsgi restart
        $ sudo service nginx restart

    4.5. debug
        $ sudo chmod 666 /var/log/uwsgi/app/producthunt.log
        $ tail /var/log/uwsgi/app/producthunt.log




