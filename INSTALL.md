intro
==================

1. Populate products from www.producthunt.com to weixin.
2. Automatically push the product list to user who follow @producthunt on weixin

setup
==================
1. utuntu 14.04
    verified on 14.04, other version should be ok too

2. run envsetup.sh to install software
    $ chmod +x ./envsetup.sh
    $ ./envsetup.sh

3. install Flask
    $ sudo pip install Flask

4. create database and tables
    $ mysql -uroot -p
    mysql> CREATE DATABASE producthunt
    mysql> source ../db/mysql.sql

deploy weixin backend first time
=======================================
deploy weixin backend by Flask + uwsgi + nginx for the first time
1. config uwsgi
    1.1 save following config in "/etc/uwsgi/app-available/weixin.xml"
    <uwsgi>
        <plugins>python</plugins>
        <master>true</master>
        <processes>4</processes>
        <no-orphans>true</no-orphans>
        <vacuum>true</vacuum>
        <chmod-socket>666</chmod-socket>
        <socket>/tmp/uwsgi.weixin.sock</socket>
        <uid>www-data</uid>
        <gid>www-data</gid>
        <pythonpath>/var/www/weixin</pythonpath>
        <module>app</module>
        <callable>app</callable>
    </uwsgi>

    1.2 enable uwsgi app
    $ cd /etc/uwsgi/app-enabled
    $ sudo ln -s ../app-available/weixin.xml .

2. config nginx
    2.1 save following config in "/etc/nginx/sites-available/weixin"
    server {
      listen 80;
      server_name 127.0.0.1;

      location / {
        include uwsgi_params;
        uwsgi_pass unix://tmp/uwsgi.weixin.sock;
      }
    }

    2.2 remove the default config:
    $ sudo rm /etc/nginx/sites-enabled/default

    2.3 enable weixin site
    $ cd /etc/nginx/sites-enabled
    $ sudo ln -s ../sites-available/weixin .

3. deploy weixin app
    $ sudo mkdir -p /var/www/
    $ sudo cp -R /path/to/prj/weixin /var/www/
    $ sudo chown -R www-data:www-data /var/www/weixin

4. start service
    $ sudo service uwsgi restart
    $ sudo service nginx restart

5. troubleshooting
    $ sudo chmod 666 /var/log/uwsgi/app/weixin.log
    $ tail /var/log/uwsgi/app/weixin.log
    $ mail me

deploy producthunt spider first time
=======================================
we use scrapyd to manage spiders, assume that you already install scrapyd
1. set deploy target in scrapy.cfg
    [deploy]
    url = http://localhost:6800/
    project = producthunt
    version = GIT
2. deploy spiders
    run "scrapy deploy" in "weixin_producthunt/producthunt" dir

3. init database
    run a spider to craw all data from producthunt.
    curl http://localhost:6800/schedule.json -d project=producthunt -d spider=comments -d maxposts=7300
    The maxposts is the max post id to crawl. You can set it a little larger than the latest postid in producthunt.com

4. schedule spider to run
    use crontab to schedule these two spider run every hour
    schedule spider to crawl products within 3 days
    curl http://localhost:6800/schedule.json -d project=producthunt -d spider=products
    schedule spider to crawl comments within 3 days
    curl http://localhost:6800/schedule.json -d project=producthunt -d spider=comments

deploy when update
=======================================
1. depoly weixin backend when update
    run "devdeploy.sh" in project root dir "weixin_producthunt"

2. deploy producthunt spider when update
    run "scrapy deploy" in spider's root dir "weixin_producthunt/producthunt"


