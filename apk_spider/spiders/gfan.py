#coding:utf-8
import scrapy
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from apk_spider.items import APKItem
import re

class APKSpider(CrawlSpider):
    name = 'gfan'
    allowed_domains = ['apk.gfan.com']
    start_urls = ['http://apk.gfan.com/games_8_1_1.html',\
                  'http://apk.gfan.com/apps_7_1_1.html']

    rules = (Rule(LinkExtractor(allow=(re.compile('apk\.gfan\.com/[A-Za-z]+_\d+_\d+_\d+.html')),)),Rule(LinkExtractor(allow=(re.compile('apk\.gfan\.com/Product/App\d+.html'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//h4[@class='curr-tit']/text()").extract())
        raw_version = ''.join(sel.xpath("//div[@class='app-info']/p[1]/text()").extract())
        index = raw_version.find("：".decode("utf-8"))
        version = raw_version[index+1:]
        item['name'] = name+' '+version
        item['url'] = sel.xpath("//a[@id='computerLoad']/@href").extract()
        raw_size = ''.join(sel.xpath("//div[@class='app-info']/p[4]/text()").extract())
        index = raw_size.find("：".decode("utf-8"))
        item['size'] = raw_size[index+1:]
        return item


