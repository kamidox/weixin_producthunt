#!/bin/bash
########################################################################################
# This file is called by fabric, please refer to fabfile.py
#
# INSTANCE_PATH: The application instance path, refer to ProductionConfig.INSTANCE_PATH, 
# database and logs will store here
# APP_ROOT_PATH: The application root path, the code form git will clone here
# APP_GIT_URL: The application git repo url
# APP_LOCAL_NAME: Application local name. Code will clone to $APP_ROOT_PATH/$APP_LOCAL_NAME
# APP_BRANCH: Branche name to deploy

INSTANCE_PATH=$1
APP_ROOT_PATH=$2
APP_GIT_URL=$3
APP_LOCAL_NAME=$4
APP_BRANCH=$5
########################################################################################

# init instance path to store database and logs
mkdir -p $INSTANCE_PATH
mkdir -p $INSTANCE_PATH/logs
mkdir -p $APP_ROOT_PATH

# clone source code
cd $APP_ROOT_PATH
git clone $APP_GIT_URL $APP_LOCAL_NAME
cd $APP_ROOT_PATH/$APP_LOCAL_NAME
git checkout $APP_BRANCH

# setup virtual env
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

# setup database
cd $APP_ROOT_PATH
python manage.py createall
python manage.py pullsample

# setup data owner and permission
sudo chown -R www-data:www-data $INSTANCE_PATH

# restart nginx and uwsgi
sudo service nginx restart
sudo service uwsgi restart


