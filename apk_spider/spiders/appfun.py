#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _AppfunApkSpider(CrawlSpider):
    name = 'appfun'
    allowed_domains = ['www.appfun.cn']
    start_urls = [\
            'http://www.appfun.cn'\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://www\.appfun\.cn/soft/applist/cid.+'),\
                            re.compile(r'http://www\.appfun\.cn/game/applist/cid.+'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://www\.appfun\.cn/app/info/appid/\d+'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='content-categoryCtn-title clearfix']/h1/text()").extract())
        size = ''.join(sel.xpath("//ul[@class='sideBar-appDetail']/li[3]/div/text()").extract())
        url = ''.join(sel.xpath("//div[@class='content-detailCtn-icon']/a/@href").extract())
        size = size.strip()

        item['name'] = name
        item['url'] = url
        item['size'] = size

        #print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(5)
        return item

