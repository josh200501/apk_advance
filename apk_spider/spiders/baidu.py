#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _BaiduApkSpider(CrawlSpider):
    name = 'baiduapk'
    allowed_domains = ['shouji.baidu.com']
    start_urls = [\
            'http://shouji.baidu.com',\
            'http://shouji.baidu.com/soft',\
            'http://shouji.baidu.com/game',\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://www\.520apk\.com/androids/paihang/soft/\d+'),\
                            re.compile(r'http://www\.520apk\.com/androis/paihang/game/\d+')\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://shouji\.baidu\.com/soft/item\?docid\=.+'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='content-right']/h1/span/text()").extract())
        size = ''.join(sel.xpath("//div[@class='detail']/span[@class='size']/text()").extract())
        url = ''.join(sel.xpath("//div[@class='area-download']/a[@data_type='apk']/@data_url").extract())
        item['name'] = name
        item['url'] = url
        item['size'] = size[4:]

        """
        length = len(size)
        for i in range(length):
            print i, size[i]
        """

        print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(5)
        return item

