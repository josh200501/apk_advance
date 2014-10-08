# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spiders import mongodb
import string
from scrapy import log

class MongoDBPipeline(object):
    def __init__(self):
        self.item_list = []
        self.NUM = 100
    def process_item(self, item, spider):
        worker = '0'
        if spider.name == '66u':
            url = ''.join(item['url'])
            name = ''.join(item['name'])
            size = ''.join(item['size'])
            if name == '' or url[-3:] != 'apk':
                return item
        url = ''.join(item['url'])
        size = ''.join(item['size'])
        if size[-1:]=='M' or size[-1:]=='K':
            item['size'] = size+'B'
        if url != '':
            if size == '':
                item['size'] == '-1MB'
            if mongodb.is_url_exist(url):
                return item
            self.item_list.append(item)
            log.msg("Processed link %s" % url,level=log.DEBUG )
            if len(self.item_list) >= self.NUM:
               # while not mongodb.set_collection_using():
               #     sleep(0.1)
                mongodb.batch_insert_to_download_candidate_list(self.item_list,worker)
               # mongodb.set_collection_free()
                self.item_list = []
#            mongodb.insert_to_download_candidate_list(item,worker)
        return item
