#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools

class A66uSpider(CrawlSpider):
    name = '66u'
    allowed_domains = ['66u.com']
    start_urls = ['http://android.66u.com/azyx/',]

    rules = (Rule(LinkExtractor(allow=(re.compile(r'http://android.66u.com/azyx/list_\d+_\d+\.html')),)),Rule(LinkExtractor(allow=(re.compile(r'http://android.66u.com/azyx/[a-z]+/\d+_\d+.html'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        item['url'] = sel.xpath("//a[@class='btn-guanfang']/@href").extract()
        item['name'] = sel.xpath("//div[@class='property']/h3/text()").extract()
        item['size'] = ''
        return item

