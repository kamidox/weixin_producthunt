# !/bin/bash
# This script used to setup runing enviroment

# install Flask
sudo apt-get install python-pip
sudo pip install Flask

# install scrapy and scrapyd
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 627220E7
echo 'deb http://archive.scrapy.org/ubuntu scrapy main' | sudo tee /etc/apt/sources.list.d/scrapy.list
sudo apt-get update
sudo apt-get install scrapy-0.25 scrapyd

# install mysql and python-mysqldb
sudo apt-get install mysql-server python-mysqldb
# setup mysql server and create database, this should do by manual
# when install mysql-server, we set the password of 'root' as 'kamidox'
# if you want to change the password, you can use following command:
# mysqladmin -uroot -pkamidox password 'your new password'
# mysql -uroot -pkamidox
# mysql> CREATE DATABASE producthunt
