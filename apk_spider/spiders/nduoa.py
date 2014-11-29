#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _NduoaApkSpider(CrawlSpider):
    name = 'nduoa'
    allowed_domains = ['www.nduoa.com']
    start_urls = [\
            'http://www.nduoa.com',\
            'http://www.nduoa.com/cat2',\
            'http://www.nduoa.com/cat1',\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://www\.nduoa\.com/cat.+'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://www\.nduoa\.com/package/detail/\d+'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        domain = 'www.nduoa.com'
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='name']/span[@class='title']/text()").extract())
        size = ''.join(sel.xpath("//div[@class='size row']/text()").extract())
        url = ''.join(sel.xpath("//div[@class='downloadWrap']/div[@class='normal']/a[1]/@href").extract())
        size = size.strip()
        url = 'http://' + domain + url

        item['name'] = name
        item['url'] = url
        item['size'] = size[3:]

        """
        for i in range(len(size)):
            print i, size[i]
        """

        print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(0.5)
        return item

