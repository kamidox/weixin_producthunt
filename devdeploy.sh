sudo rm -R /var/www/weixin
sudo cp -R weixin /var/www/
sudo chown -R www-data:www-data /var/www/weixin
sudo service uwsgi reload
