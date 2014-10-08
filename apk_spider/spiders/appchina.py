#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools

class AppchinaSpider(CrawlSpider):
    name = 'appchina'
    allowed_domains = ['www.appchina.com']
    start_urls = ['http://www.appchina.com/category/30.html',\
                  'http://www.appchina.com/category/40.html']

    rules = (Rule(LinkExtractor(allow=(re.compile(r'/category/30/.+\.html'),re.compile(r'/category/40/.+\.html')),)),Rule(LinkExtractor(allow=(re.compile(r'/app/com.*'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath('//h1[@class="app-name"]/text()').extract())
        item['name'] = name
        raw_size = ''.join(sel.xpath('//span[@class="app-statistic"]/text()').extract())
        index1 = raw_size.find('：'.decode('utf-8'))
        index2 = raw_size.find('更新'.decode('utf-8'))
        item['size'] = raw_size[index1+1:index2-1]
        item['url'] = ''.join(sel.xpath("//a[@class='app-download']/@href").extract())

        return item

