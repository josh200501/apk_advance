#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _MyappApkSpider(CrawlSpider):
    name = 'myapp'
    allowed_domains = ['android.myapp.com']
    start_urls = [\
            'http://android.myapp.com/myapp/category.htm?orgname=1',\
            'http://android.myapp.com/myapp/category.htm?orgname=2'\
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
                            re.compile(r'http://android\.myapp\.com/myapp/detail.htm\?apkName.+'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='det-name-int']/text()").extract())
        size = ''.join(sel.xpath("//div[@class='det-size']/text()").extract())
        url = ''.join(sel.xpath("//div[@class='det-ins-btn-box']/a[@class='det-down-btn']/@data-apkurl").extract())
        item['name'] = name
        item['url'] = url
        item['size'] = size

        #print '[-]', 'name: ', name.encode('utf-8'), 'url: ', url, 'size: ', size
        time.sleep(5)
        return item

