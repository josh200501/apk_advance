#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _25ppApkSpider(CrawlSpider):
    name = '25pp'
    allowed_domains = ['android.25pp.com']
    start_urls = [\
            'http://android.25pp.com'\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://android\.25pp\.com/software/.+'),\
                            re.compile(r'http://android\.25pp\.com/game/.+'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://android\.25pp\.com/detail.+'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='title-stat']/div[@class='txt']/h1/text()").extract())
        size = ''.join(sel.xpath("//div[@class='title-stat']/div[@class='txt']/ul/li[3]/text()").extract())
        url = ''.join(sel.xpath("//div[@class='aoubtL']/a/@href").extract())
        size = size.strip()

        item['name'] = name
        item['url'] = url
        item['size'] = size[4:]

        #print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(5)
        return item

