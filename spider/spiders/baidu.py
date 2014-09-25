#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools

class BaiduSpider(CrawlSpider):
    name = 'baidu'
    allowed_domains = ['as.baidu.com']
    start_urls = ['http://as.baidu.com/a/asgame?cid=102&s=1','http://as.baidu.com/a/software?cid=101&s=1']

    rules = (Rule(LinkExtractor(allow=(re.compile(r'http://as.baidu.com/a/asgame\?cid=\d+&s=\d+&pn=\d+'),re.compile(r'http://as.baidu.com/a/software\?cid=\d+&s=\d+&f=asgame_\d+_\d*&pn=\d+')),)),Rule(LinkExtractor(allow=(re.compile(r'http://as.baidu.com/a/item\?docid=\d+&pre=web_am_[a-z]*&pos=[a-z]+_\d+_\d+&f=[a-z]+_\d+_\d+'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        item['url'] = sel.xpath("//td[@class='col-content']/a[@target='_blank']/@href").extract()
        item['name'] = sel.xpath("//span[@id='appname']/text()").extract()
        item['size'] = sel.xpath("//dd[@class='info-params']/table[1]/tbody[1]/tr[1]/td[1]/span/text()").extract()
        return item

