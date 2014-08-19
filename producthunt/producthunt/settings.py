# -*- coding: utf-8 -*-

# Scrapy settings for producthunt project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

#LOG_LEVEL = 'INFO'

BOT_NAME = 'producthunt'

SPIDER_MODULES = ['producthunt.spiders']
NEWSPIDER_MODULE = 'producthunt.spiders'

ITEM_PIPELINES = [
    'producthunt.pipelines.RequiredFieldsPipeline',
    'producthunt.pipelines.MySQLStorePipeline',
]

# database
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'producthunt'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'kamidox'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'producthunt (+http://www.yourdomain.com)'
