# -*- coding: utf-8 -*-

# Scrapy settings for apk_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import scrapy
import os

BOT_NAME = 'apk_spider'

SPIDER_MODULES = ['apk_spider.spiders']
NEWSPIDER_MODULE = 'apk_spider.spiders'

COMMANDS_MODULE = 'apk_spider.commands'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'apk_spider (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0'

ITEM_PIPELINES = {
        'apk_spider.pipelines.MongoDBPipeline'
        }


#LOG_ENABLED = True
#LOG_FILE = os.getcwd()+'/log/spider.log'
LOG_LEVEL = scrapy.log.DEBUG

#WEBKIT_DOWNLOADER=['ccb']
#DOWNLOADER_MIDDLEWARES= {
#        'apk_spider.downloadmiddleware.WebkitDownloader':543
#        }

