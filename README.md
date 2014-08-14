weixin_producthunt
==================

1. Populate products from www.producthunt.com to weixin.
2. Automatically push the product list to user who follow @producthunt on weixin

setup
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

