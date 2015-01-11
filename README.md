# ProductPorter

## intro

Let cool products embrace China

## setup

1. Install Wechat(weixin) in your mobile phone
2. Follow "producthunt" on Wechat(weixin) public account

## usage

1. search:keyword - search products base on keyword
2. 1/2/3 - view top voted products by day/week/month

Send 'help' in Wechat(weixin) to producthunt to get help information

## setup development environment

* Create a virtualenv
    * `cd weixin_producthunt`
    * `virtualenv .venv`
    * `source .venv/bin/activate`
* Install the dependencies
    * `pip install -r requirements.txt`
* Configuration (_adjust them accordingly to your needs_)
    * For development copy `productporter/configs/development.py.example` to `productporter/configs/development.py`
* Database creation
    * `python manage.py createall`
* Run the development server
    * `python manage.py runserver`
* Visit [localhost:5000/porter/posts](http://localhost:5000/porter/posts)

## deploy

* copy `fabfile.py.example` to `fabfile.py`, modify accordingly
* copy `deploy/production.py.example` to `deploy/production.py` and modify accordingly

### bootstrap deploy

If you deploy the first time or setup a new server instance. Please follow these steps:

* install nginx/uwsgi/pip and other tools.
    `sudo apt-get -y install python-pip nginx-full uwsgi uwsgi-plugin-python`
* setup nginx config file on remote server, please refer to `deploy/nginxconf.example`
* setup uwsgi config file on remote server, please refer to `deploy/uwsgiconf.example`
* run `fab -H newserver.example.com bootstrap`
* create a crontab to pull products periodic

### production

Since SQLite do not support Flask-Migrate, we sugguest to use mysql in production mode.

* install mysql and mysqldb.
    `sudo apt-get -y install mysql-server python-mysqldb`
* create database before bootstrap deploy
    use `mysql -uuser -ppassword` to connect mysql database; and use `CREATE DATABASE productporter;` to create database named **productporter**.

### continuous deploy

* run `fab deploy`

### more on deploy

I deploy this app in aws by nginx + uwsgi. Explain more about the nginx config and uwsgi config. For `deploy/nginxconf.example`, I deploy multi app in one aws instance. This app is deploy in `kamidox.com/pp` as:

```text
    location /pp/ {
        include uwsgi_params;
        uwsgi_pass unix://tmp/uwsgi.pp.sock;
    }
```

For uwsgi, it's important to note the following parameters:

```xml
    <virtualenv>/home/kamidox/work/weixin_producthunt/.venv</virtualenv>
    <pythonpath>/home/kamidox/work/weixin_producthunt</pythonpath>
    <module>run</module>
    <callable>app</callable>
```

`virtualenv` to setup the virtualenv of the app. uwsgi will look for `run.py` in `/home/kamidox/work/weixin_producthunt` and find the object called `app` and call `app.run()` to launch application.



