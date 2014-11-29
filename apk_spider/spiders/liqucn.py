#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _LiqucnApkSpider(CrawlSpider):
    name = 'liqucn'
    allowed_domains = ['os-android.liqucn.com']
    start_urls = [\
            'http://os-android.liqucn.com/rj/',\
            'http://os-android.liqucn.com/yx/',\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://os-android\.liqucn\.com/rj/c/\d+/'),\
                            re.compile(r'http://os-android\.liqucn\.com/yx/c/\d+/'),\
                            re.compile(r'http://os-android\.liqucn\.com/rj/index_.+/'),\
                            re.compile(r'http://os-android\.liqucn\.com/yx/index_.+/'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://os-android\.liqucn\.com/rj/\d+\..+'),\
                            re.compile(r'http://os-android\.liqucn\.com/yx/\d+\..+'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='app_boxcon']/h1/text()").extract())
        size = ''.join(sel.xpath("//div[@class='app_boxcon']/table/tr[1]/td[2]/text()").extract())
        url = ''.join(sel.xpath("//div[@class='app_infobtm']/em[@class='btn_apk']/a/@href").extract())
        size = size.strip()

        item['name'] = name.strip()
        item['url'] = url
        item['size'] = size[3:]

        """
        for i in range(len(size)):
            print i, size[i]
        """

        print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        #time.sleep(0.5)
        return item

