#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _PconlineApkSpider(CrawlSpider):
    name = 'pconline'
    allowed_domains = ['dl.pconline.com.cn']
    start_urls = [\
            'http://dl.pconline.com.cn/sort/1402.html'\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://dl\.pconline\.com\.cn/sort/1402-\d+-\d+\.html'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://dl\.pconline\.com\.cn/download/\d+\.html'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        print 'response: ', response
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='thead']/span/h1/text()").extract())
        size = ''.join(sel.xpath("//ul[@class='megList']/li[1]/i[2]/span[2]/text()").extract())
        url = ''.join(sel.xpath("//div[@class='dlLink']/div[@class='megL']/a").extract())
        size = size.strip()

        item['name'] = name
        item['size'] = size
        item['url'] = url

        print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        #time.sleep(0.5)
        return item

