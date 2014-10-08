#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools

class Apk8Spider(CrawlSpider):
    name = 'apk8'
    allowed_domains = ['www.apk8.com']
    start_urls = ['http://www.apk8.com/game/list_1.html',\
                  'http://www.apk8.com/wy/list_1.html',\
                  'http://www.apk8.com/soft/list_1.html']

    rules = (Rule(LinkExtractor(allow=(re.compile(r'.*/game/list_\d+\.html'),re.compile(r'.*/wy/list_\d+\.html'),re.compile(r'.*/soft/list_\d+\.html')),)),Rule(LinkExtractor(allow=(re.compile(r'http://www\.apk8\.com/game/game_\d+.html'),re.compile(r'http://www\.apk8\.com/soft/soft_\d+\.html'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        item['url'] = ''.join(sel.xpath("//a[@class='bt_bd']/@href").extract())
        version = ''.join(sel.xpath("//div[@class='detailsleft']/ol[1]/li[1]/text()").extract())
        name = ''.join(sel.xpath("//div[@class='tit_b']/text()").extract())
        item['name'] = name+" "+version
        item['size'] = ''.join(sel.xpath("//div[@class='detailsleft']/ol[3]/li[1]/text()").extract())

        return item

