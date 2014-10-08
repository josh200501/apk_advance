#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools

class AngeeksSpider(CrawlSpider):
    name = 'angeeks'
    allowed_domains = ['angeeks.com']
    start_urls = ['http://apk.angeeks.com/list/c-8-1-1.html',\
                  'http://apk.angeeks.com/list/c-4-1-1.html']

    rules = (Rule(LinkExtractor(allow=(re.compile(r'http://apk\.angeeks\.com/list/c-\d+-\d+-\d+\.html')),)),Rule(LinkExtractor(allow=(re.compile(r'/soft/\d+\.html'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath('//dl[@class="clear_div hr"]/dd[1]/a[@class="title"]/text()').extract())
        raw_version = ''.join(sel.xpath('//dl[@class="clear_div hr"]/dd[1]/span[@class="ko"]/text()').extract())
        index = raw_version.find('：'.decode("utf-8"))
        version = raw_version[index+1:]
        item['name'] = name+' '+version

        raw_size = ''.join(sel.xpath('//div[@class="rgmainslx"]/span[1]/text()').extract())
        index = raw_size.find("：".decode("utf-8"))
        size = raw_size[index+1:]
     #   size = size.strip("\r")
     #   size = size.strip("\n")
     #   size1 = size.strip("\t")
        size = size.replace("\r","")
        size = size.replace("\t","")
        size = size.replace("\n","")
        size = size.replace(" ","")
        item['size'] = size

        item['url'] = ''.join(sel.xpath('//div[@class="rgmainsr"]/div[1]/a[1]/@href').extract())

        return item

