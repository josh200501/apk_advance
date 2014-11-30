#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _AndroidonlineApkSpider(CrawlSpider):
    name = 'androidonline'
    allowed_domains = ['www.androidonline.net']
    start_urls = [\
            'http://www.androidonline.net'\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://www\.androidonline\.net/soft/list/.+'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://www\.androidonline\.net/soft/\d+\.html'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        domain = 'www.androidonline.net'
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='downInfoTitle']/text()").extract())
        size = ''.join(sel.xpath("//dd[@class='downInfoRowL']/ul[@id='downinfobox']/li[1]/text()").extract())
        url = ''.join(sel.xpath("//ul[@class='downlistbox']/li[1]/a/@href").extract())
        size = size.strip()
        url = 'http://' + domain + url

        item['name'] = name
        item['size'] = size[5:]
        item['url'] = url

        #print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(5)
        return item

