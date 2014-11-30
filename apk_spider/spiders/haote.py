#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _HaoteApkSpider(CrawlSpider):
    name = 'haote'
    allowed_domains = ['www.haote.com']
    start_urls = [\
            'http://www.haote.com/SoftList/909_1.html'\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://www\.haote\.com/SoftList/909_\d+\.html'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://www\.haote\.com/xz/\d+\.html'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='htDdTitleIn']/h1/em/text()").extract())
        size = ''.join(sel.xpath("//ul[@class='htDdList']/li[1]/span/text()").extract())
        url = ''.join(sel.xpath("//div[@class='htDl']/a/@href").extract())
        size = size.strip()

        item['name'] = name
        item['size'] = size
        item['url'] = url

        #print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(5)
        return item

