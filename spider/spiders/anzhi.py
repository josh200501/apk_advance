#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools

class AnzhiSpider(CrawlSpider):
    name = 'anzhi'
    allowed_domains = ['anzhi.com']
    start_urls = ['http://www.anzhi.com/list_1_1_new.html','http://www.anzhi.com/list_2_1_new.html','http://www.anzhi.com/list_1_1_hot.html']

    rules = (Rule(LinkExtractor(allow=(re.compile(r'http://www.anzhi.com/list_\d*_\d*_[a-z]*.html')),)),Rule(LinkExtractor(allow=(re.compile(r'http://www.anzhi.com/soft_\d*.html'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        click = ''.join(sel.xpath("//div[@class='detail_down']/a/@onclick").extract())
        t = re.findall(r'\(.*?\)',click)
        number_id = eval(t[0])
        s = 'http://www.anzhi.com:80/dl_app.php?s=%s&n=5' % number_id
        item['url'] = s
        n1 = ''.join(sel.xpath("//div[@class='detail_line']/h3/text()").extract())
        n2 = ' '.join(sel.xpath("//span[@class='app_detail_version']/text()").extract())
        n1 = n1 + n2
        item['name'] = n1
        item['size'] = ''
        return item

