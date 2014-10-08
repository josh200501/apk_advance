#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools

class HiapkSpider(CrawlSpider):
    name = 'hiapk'
    allowed_domains = ['apk.hiapk.com']
    start_urls = ['http://apk.hiapk.com/apps',\
                  'http://apk.hiapk.com/games']

    rules = (Rule(LinkExtractor(allow=(re.compile(r'http://apk\.hiapk\.com/apps\?sort=5&pi=\d+'),re.compile(r'http://apk\.hiapk\.com/games\?sort=5&pi=\d+')),)),Rule(LinkExtractor(allow=(re.compile(r'http://apk\.hiapk\.com/appinfo/.+'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='left detail_description']/div[@id='appSoftName']/text()").extract())
        name = name.replace('\n','')
        name = name.replace(' ','')
        item['name'] = name
        item['url'] = 'http://apk.hiapk.com'+''.join(sel.xpath("//div[@class='code_box_border']/div[10]/a/@href").extract())
        item['size'] = ''.join(sel.xpath("//div[@class='code_box_border']/div[4]/span[@id='appSize']/text()").extract())
        return item

