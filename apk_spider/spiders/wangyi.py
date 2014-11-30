#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _WangyiApkSpider(CrawlSpider):
    name = 'wangyi'
    allowed_domains = ['m.163.com']
    start_urls = [\
            'http://m.163.com/android/category/allapp/index.html',\
            'http://m.163.com/android/game/allgame/index.html',\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://m\.163\.com/android/category/allapp/all-download-\d+\.html'),\
                            re.compile(r'http://m\.163\.com/android/game/allgame/all-download-\d+\.html'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://m\.163\.com/android/software/.+\.html'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='sect-main-s-inner p-t15']/h1/span/text()").extract())
        size = ''.join(sel.xpath("//div[@class='sect-side-s']/div[@class='t-c p-t20']/p[@class='m-t20 c-gray']/text()").extract())
        url = ''.join(sel.xpath("//div[@class='arti-bd-content']/div[@class='clearfix']/div[@class='sect-side-s']/div[@class='t-c p-t20']/p[@class='m-t15']/a[@class='btn-download-byandroid']/@href").extract())

        size = size.strip()

        name = name.strip()

        item['name'] = name
        item['size'] = size[3:]
        item['url'] = url

        #print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(5)
        return item

