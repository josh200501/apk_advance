#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _SogouApkSpider(CrawlSpider):
    name = 'sogou'
    allowed_domains = ['app.sogou.com']
    start_urls = [\
            'http://app.sogou.com/soft',\
            'http://app.sogou.com/game'\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://app\.sogou\.com/soft/\d+/0/1.+'),\
                            re.compile(r'http://app\.sogou\.com/game/\d+/0/1.+')\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://app\.sogou\.com/detail/\d+'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='d-title cf']/em[@class='title cf']/@title").extract())
        size = ''.join(sel.xpath("//div[@class='content']/ul[@class='dd cf']/li[3]/text()").extract())
        url = ''.join(sel.xpath("//a[@class='down_pc_btn']/@href").extract())

        size = size.strip()

        name = name.strip()

        item['name'] = name
        item['size'] = size[3:]
        item['url'] = url

        #print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(5)
        return item

