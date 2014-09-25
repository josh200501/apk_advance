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
#        if spider.name == 'www.mumayi.com':
#            mongodb.insert_to_download_candidate_list(item,worker)
        if spider.name == '66u':
           #filter the item 
            url = ''.join(item['url'])
            name = ''.join(item['name'])
            if name == '' or url[-3:] != 'apk':
                return item
        if spider.name == 'baidu':
            size = ''.join(item['size'])
            size = size[:-2]
            num_size = string.atof(size)
            if num_size > 32:
                return item
#        if spider.name == 'dl.pconline.com.cn':

#        if spider.name == 'www.anzhi.com':
        url = ''.join(item['url'])
        if url != '':
            mongodb.insert_to_download_candidate_list(item,worker)
	log.msg("Processed link %s" % url,level=log.INFO )
        return item
