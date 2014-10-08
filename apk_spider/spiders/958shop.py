#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools

class _958ShopSpider(CrawlSpider):
    name = '958shop'
    allowed_domains = ['958shop.com']
    start_urls = ['http://d.958shop.com/format/soft/0-89/',\
                  'http://d.958shop.com/format/game/0-113/']

    rules = (Rule(LinkExtractor(allow=(re.compile(r'http://d\.958shop\.com/format/soft/0-89/\d+/0/'),re.compile(r'http://d\.958shop\.com/format/game/0-113/\d+/0/')),)),Rule(LinkExtractor(allow=(re.compile(r'http://d\.958shop\.com/soft/.+\.html'),re.compile(r'http://d\.958shop\.com/game/.+\.html'))),callback='parse_item'),)

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = sel.xpath('//div[@class="infor_word"]/div[@class="detail_m"]/table[@class="m_word"]/tr[1]/td[1]/span[1]/text()').extract()
        item['name'] = name

        raw_size = ''.join(sel.xpath('//div[@class="detail_m"]/table[@class="m_word"]/tr[5]/td[1]/text()').extract())
        index = raw_size.find("：".decode('utf-8'))
        size = raw_size[index+1:]
        item['size'] = size

        item['url'] = ''.join(sel.xpath('//dd[@class="down_u_1"]/a[2]/@href').extract())

        return item

