#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _SkycnApkSpider(CrawlSpider):
    name = 'skycn'
    allowed_domains = ['sj.skycn.com']
    start_urls = [\
            'http://sj.skycn.com/android/'\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://sj\.skycn\.com/android/0_1_\d+\.html'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://sj\.skycn\.com/\d+\.html'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='soft-title']/h1/text()").extract())
        size = ''.join(sel.xpath("//ul[@class='soft-info-list']/li[1]/div[1]/text()").extract())
        url = ''.join(sel.xpath("//div[@class='soft-dl-button  soft-dl-nobr']/a/@href").extract())
        size = size.strip()

        item['name'] = name
        item['size'] = size[3:]
        item['url'] = url

        #print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(5)
        return item

