#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _TgbusApkSpider(CrawlSpider):
    name = 'tgbus'
    allowed_domains = ['a.tgbus.com']
    start_urls = [\
            'http://a.tgbus.com/soft/list-0-0-0-1/'\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://a\.tgbus\.com/soft/list-0-0-0-1/\d+/'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://a\.tgbus\.com/soft/item-\d+/'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        #name = ''.join(sel.xpath("//div[@class='content-categoryCtn-title clearfix']/h1/text()").extract())
        #size = ''.join(sel.xpath("//ul[@class='sideBar-appDetail']/li[3]/div/text()").extract())
        url = ''.join(sel.xpath("//div[@id='TGBUS_VISTA_CONTAINER_234']/div/a/@href").extract())
        #size = size.strip()

        item['name'] = 'null'
        item['size'] = 0
        item['url'] = url

        print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(0.5)
        return item

