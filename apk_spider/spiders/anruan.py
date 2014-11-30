#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _AnruanApkSpider(CrawlSpider):
    name = 'anruan'
    allowed_domains = ['soft.anruan.com', 'game.anruan.com']
    start_urls = [\
            'http://soft.anruan.com/index_1.html',\
            'http://soft.anruan.com/new/',\
            'http://soft.anruan.com/hot/',\
            'http://game.anruan.com/index_1.html',\
            'http://game.anruan.com/gnew/',\
            'http://game.anruan.com/ghot/'\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://soft\.anruan\.com/index_\d+\.html'),\
                            re.compile(r'http://soft\.anruan\.com/hot/index_\d+\.html'),\
                            re.compile(r'http://soft\.anruan\.com/new/index_\d+\.html'),\
                            re.compile(r'http://game\.anruan\.com/index_\d+\.html'),\
                            re.compile(r'http://game\.anruan\.com/ghot/index_\d+\.html'),\
                            re.compile(r'http://game\.anruan\.com/gnew/index_\d+\.html'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://soft\.anruan\.com/\d+/'),\
                            re.compile(r'http://game\.anruan\.com/g-\d+/'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='pn2 appun']/div[@class='pa']/div[@class='pc']/h1/text()").extract())
        size = ''.join(sel.xpath("//div[@class='app_info']/div[@class='c0']/ul[@class='c1']/li[6]/text()").extract())
        url = ''.join(sel.xpath("//div[@class='app_info']/ul[@class='c2']/li[@class='app_down'][1]/a[@class='ldownload']/@href").extract())

        size = size.strip()

        name = name.strip()

        item['name'] = name
        item['size'] = size
        item['url'] = url

        #print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(5)
        return item

