#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools

class UzzfSpider(CrawlSpider):
    name = 'uzzf'
    allowed_domains = ['uzzf.com']
    start_urls = ['http://www.uzzf.com/apk/r_104_1.html',\
                  'http://www.uzzf.com/apk/r_106_1.html']

    rules = (Rule(LinkExtractor(allow=(re.compile(r'http://www\.uzzf\.com/apk/r_104_\d+\.html'),re.compile(r'http://www\.uzzf\.com/apk/r_106_\d+\.html')),)),Rule(LinkExtractor(allow=(re.compile(r'http://www\.uzzf\.com/apk/\d+\.html'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath('//h1[@class="app-title"]/text()').extract())
        version = ''.join(sel.xpath('//h1[@class="app-title"]/span[1]/text()').extract())
        item['name'] = name + version
        
        raw_size = ''.join(sel.xpath("//ul[@class='info-list']/li[3]/text()").extract())
        index = raw_size.find("：".decode('utf-8'))
        size = raw_size[index+1:]
        item['size'] = size

        item['url'] = ''.join(sel.xpath("//ul[@class='downbtn-wrap fl pr']/li[1]/a[1]/@href").extract())
        return item

