#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _FpwapApkSpider(CrawlSpider):
    name = 'fpwap'
    allowed_domains = ['www.fpwap.com']
    start_urls = [\
            'http://www.fpwap.com/gamelist/2-0-0-0-0-0-1.html'\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://www\.fpwap\.cn/ruanjian/list_.+'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://www\.paojiao\.cn/ruanjian/detail_\d+\.html'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='detail_content']/h2/text()").extract())
        size = ''.join(sel.xpath("//div[@class='detail-box']/div[@class='center']/ul[@class='info']/li[1]/text()").extract())
        url = ''.join(sel.xpath("//a[@class='downbtn1']/@href").extract())

        url_new = url.split("'")

        size = size.strip()

        name = name.strip()
        name = name.replace("\r", "")
        name = name.replace("\n", "")
        name = name.replace("\t", "")

        item['name'] = name
        item['size'] = size
        item['url'] = url_new[1]

        print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(0.5)
        return item

