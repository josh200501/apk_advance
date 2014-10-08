#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _91Spider(CrawlSpider):
    name = '91'
    allowed_domains = ['apk.91.com']
    start_urls = ['http://apk.91.com/soft/',\
                  'http://apk.91.com/game/']

    rules = (Rule(LinkExtractor(allow=(re.compile(r'/soft/\d+_\d+_\d+'),re.compile(r'/game/\d+_\d+_\d+')),)),Rule(LinkExtractor(allow=(re.compile(r'/Soft/Android/.+\.html'),)),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response) 
        name = ''.join(sel.xpath("//div[@class='s_title clearfix']/h1[1]/text()").extract())
        name  = name.replace(' ','')
        name = name.strip('\t')
        name = name.strip('\r')
        name = name.strip('\n')
        item['name'] = name
        raw_size = ''.join(sel.xpath("//ul[@class='s_info']/li[3]/text()").extract())
        index = raw_size.find("：".decode('utf-8'))
        item['size'] = raw_size[index+1:]
        raw_url = ''
        raw_url = ''.join(sel.xpath("//a[@class='s_btn s_btn4']/@href").extract())
        item['url'] = 'http://apk.91.com'+raw_url
       
        time.sleep(10)

        return item

