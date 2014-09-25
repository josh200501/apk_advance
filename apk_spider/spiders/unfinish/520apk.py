#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _520ApkSpider(CrawlSpider):
    name = '520apk'
    allowed_domains = ['www.520apk.com']
    start_urls = ['http://www.520apk.com/androids/paihang/soft/',\
                  'http://www.520apk.com/androids/paihang/game/']

    rules = (Rule(LinkExtractor(allow=(re.compile(r'http://www\.520apk\.com/androids/paihang/soft/\d+'),re.compile(r'http://www\.520apk\.com/androis/paihang/game/\d+')),)),Rule(LinkExtractor(allow=(re.compile(r'http://www\.520apk\.com/android/.+/\d+\.html'),)),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response) 
        item['name'] = ''.join(sel.xpath("//div[@class='detail-title']/h1[@id='view_name']/text()").extract())
        item['url'] = ''.join(sel.xpath("//div[@id='downurl']/div[@class='dl-box']/div[2]//ul[1]/li[4]/@href").extract())
        raw_size = ''.join(sel.xpath("//div[@class='detailsleft']/ol[1]/li[2]/text()").extract())
        item['size'] = ''.join(sel.xpath("//div[@class='detail-box']/div[@class='center']/span[@id='view_size']/i[1]/text()").extract())
        time.sleep(5000)
        return item

