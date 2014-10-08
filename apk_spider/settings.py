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

BOT_NAME = 'baidu'

SPIDER_MODULES = ['apk_spider.spiders']
NEWSPIDER_MODULE = 'apk_spider.spiders'

#COMMANDS_MODULE = 'apk_spider.commands'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0'

ITEM_PIPELINES = {
        'apk_spider.pipelines.MongoDBPipeline'
        }


LOG_ENABLED = True
LOG_FILE = os.getcwd()+'/log/spider.log'
LOG_LEVEL = scrapy.log.ERROR

#AUTOTHROTTLE_ENABLED = True
#CONCURRENT_REQUESTS_PER_IP = 4

#MEMUSAGE_ENABLED = True
#MEMUSAGE_LIMIT_MB = 1024
#MEMUSAGE_NOTIFY_MAIL = ['uniquegx@qq.com']
#WEBKIT_DOWNLOADER=['ccb']
#DOWNLOADER_MIDDLEWARES= {
#        'apk_spider.downloadmiddleware.WebkitDownloader':543
#        }

