#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools

class MumayiSpider(CrawlSpider):
    name = 'mumayi'
    allowed_domains = ['mumayi.com']
    start_urls = ['http://www.mumayi.com/plus/today.php',]

    rules = (Rule(LinkExtractor(allow=('/plus/today\.php',),)),Rule(LinkExtractor(allow=(re.compile(r'www.mumayi.com/android-\d+.html'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        item['name'] = sel.xpath("//a[@class='download fl']/@title").extract()
        item['url'] = sel.xpath("//a[@class='download fl']/@href").extract()
        item['size'] = sel.xpath("//ul[@class='istyle fl']/li[4]/text()").extract()
        print item
        return item

