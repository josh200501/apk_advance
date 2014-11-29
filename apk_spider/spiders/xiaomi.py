#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _XiaomiApkSpider(CrawlSpider):
    name = 'xiaomi'
    allowed_domains = ['app.mi.com']
    start_urls = [\
            'http://app.mi.com',\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://app\.mi\.com/category/\d+'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://app\.mi\.com/detail/\d+'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        domain = 'app.mi.com'
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='intro-titles']/h3/text()").extract())
        size = ''.join(sel.xpath("//div[@class='details preventDefault']/ul[@class=' cf']/li[2]/text()").extract())
        url = ''.join(sel.xpath("//div[@class='app-info-down']/a/@href").extract())
        size = size.strip()
        url = 'http://' + domain + url

        item['name'] = name
        item['url'] = url
        item['size'] = size

        """
        for i in range(len(size)):
            print i, size[i]
        """

        print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(0.5)
        return item

