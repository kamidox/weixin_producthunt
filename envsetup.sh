# !/bin/bash
# This script used to setup runing enviroment

# add scrapy source
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 627220E7
echo 'deb http://archive.scrapy.org/ubuntu scrapy main' | sudo tee /etc/apt/sources.list.d/scrapy.list
sudo apt-get update
# install software
sudo apt-get -y install scrapy-0.25 scrapyd python-pip mysql-server python-mysqldb
