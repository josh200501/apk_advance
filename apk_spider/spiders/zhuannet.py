#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools

class ZhuannetSpider(CrawlSpider):
    name = 'zhuannet'
    allowed_domains = ['apk.zhuannet.com']
    start_urls = ['http://apk.zhuannet.com/soft/',\
                  'http://apk.zhuannet.com/game/']


    rules = (Rule(LinkExtractor(allow=(re.compile(r'http://apk\.zhuannet\.com/soft/\d+_\d+\.html'),re.compile(r'http://apk\.zhuannet\.com/game/\d+_\d+\.html')),)),Rule(LinkExtractor(allow=(re.compile(r'http://apk\.zhuannet\.com/soft/\d+\.html'),re.compile(r'http://apk\.zhuannet\.com/game/\d+\.html'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        item['url'] = ''.join(sel.xpath("//div[@class='detail2_3']/a[1]/@href").extract())
        item['name'] = ''.join(sel.xpath("//div[@class='detail2_1_left']/h1[1]/text()").extract())
        size = ''.join(sel.xpath("//div[@class='detail2_1_left']/dl[1]/dd[5]/text()").extract())
        if size[-1:]=='B' or size[-1:]=='b' or size[-1:]=='M' or size[-1:]=='m' or size[-1:]=='K' or size[-1:]=='k':
            item['size'] = size
        else:
            item['size'] = '-1MB'
        return item

