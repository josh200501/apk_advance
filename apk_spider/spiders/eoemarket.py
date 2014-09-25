#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools

class EoemarketSpider(CrawlSpider):
    name = 'eoemarket'
    allowed_domains = ['www.eoemarket.com']
    start_urls = ['http://www.eoemarket.com/soft/1_hot_unofficial_hasad_1_1.html',\
                  'http://www.eoemarket.com/game/2_hot_unofficial_hasad_2_1.html']

    rules = (Rule(LinkExtractor(allow=(re.compile(r'http://www\.eoemarket\.com/soft/1_hot_unofficial_hasad_1_\d+\.html'),re.compile(r'http://www\.eoemarket\.com/game/2_hot_unofficial_hasad_2_\d+\.html')),)),Rule(LinkExtractor(allow=(re.compile(r'http://www\.eoemarket\.com/game/\d+\.html'),re.compile(r'http://www\.eoemarket\.com/soft/\d+\.html'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response) 
        name = ''.join(sel.xpath("//div[@class='detailsleft']/div[1]/h2/text()").extract())
        raw_version = ''.join(sel.xpath("//div[@class='detailsleft']/ol[1]/li[3]/span/text()").extract())
        index = raw_version.find("：".decode('utf-8'))
        version = raw_version[index+1:]
        item['name'] = name + ' ' + version
        item['url'] = ''.join(sel.xpath("//div[@class='detailsright']/ol[1]/li[1]/a[1]/@href").extract())
        raw_size = ''.join(sel.xpath("//div[@class='detailsleft']/ol[1]/li[2]/text()").extract())
        index = raw_size.find("：".decode('utf-8'))
        item['size'] = raw_size[index+1:]

        return item

