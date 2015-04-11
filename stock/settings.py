# -*- coding: utf-8 -*-

# Scrapy settings for stock project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'stock'

SPIDER_MODULES = ['stock.spiders']
NEWSPIDER_MODULE = 'stock.spiders'
ITEM_PIPELINES = ['stock.pipelines.MongoDBPipeline',]

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "stock"
MONGODB_COLLECTION = "event"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'stock (+http://www.yourdomain.com)'
