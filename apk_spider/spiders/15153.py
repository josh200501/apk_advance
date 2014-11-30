#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _15153ApkSpider(CrawlSpider):
    name = '15153'
    allowed_domains = ['android.15153.com']
    start_urls = ['http://android.15153.com/soft/','http://android.15153.com/game/']

    rules = (Rule(LinkExtractor(allow=(re.compile(r'http://android.15153.com/soft/list.+'),),)),Rule(LinkExtractor(allow=(re.compile(r'http://android\.15153\.com/app/\d+'),re.compile(r'http://android\.15153\.com/soft/lt/\d+'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='w360 h20 f18 lh20 ']/h1/text()").extract())
        size = ''.join(sel.xpath("//div[@class='xqxx_c_c_b']/div[@class='lh20']/text()").extract())
        url = ''.join(sel.xpath("//div[@class='xqxx_c_d_a']/a/@href").extract())

        item['name'] = name
        item['size'] = size[5:]
        item['url'] = url
        #print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(5)
        return item

