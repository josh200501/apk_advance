# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spiders import mongodb
import string
from scrapy import log

class MongoDBPipeline(object):
    def process_item(self, item, spider):
        worker = '0'
        if spider.name == '66u':
            url = ''.join(item['url'])
            name = ''.join(item['name'])
            size = ''.join(item['size'])
            if name == '' or url[-3:] != 'apk':
                return item
        if spider.name == 'gfan':
            pass
        url = ''.join(item['url'])
        size = ''.join(item['size'])
        if url != '':
            if size == '':
                item['size'] == '-1MB'
            if mongodb.is_url_exist(url):
                return item
            mongodb.insert_to_download_candidate_list(item,worker)
        log.msg("Processed link %s" % url,level=log.INFO )
        return item
