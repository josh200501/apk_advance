#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _DangleApkSpider(CrawlSpider):
    name = 'dangle'
    allowed_domains = ['android.d.cn']
    start_urls = [\
            'http://android.d.cn/software',\
            'http://android.d.cn/game'\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://android\.d\.cn/software/1/-1/-1/\d+/'),\
                            re.compile(r'http://android\.d\.cn/game/1/-1/-1/\d+/')\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://android\.d\.cn/software/\d+\.html'),\
                            re.compile(r'http://android\.d\.cn/game/\d+\.html')\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        #name = ''.join(sel.xpath("//div[@class='d-title cf']/em[@class='title cf']/@title").extract())
        #size = ''.join(sel.xpath("//div[@class='content']/ul[@class='dd cf']/li[3]/text()").extract())
        url = ''.join(sel.xpath("//div[@class='de-has-set clearfix']/ul/li[1]/a").extract())

        #size = size.strip()

        #name = name.strip()

        item['name'] = 'null'
        item['size'] = 0
        item['url'] = url

        print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(0.5)
        return item

