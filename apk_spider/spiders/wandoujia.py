#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _WandoujiaApkSpider(CrawlSpider):
    name = 'wandoujia'
    allowed_domains = ['www.wandoujia.com']
    start_urls = [\
            'http://www.wandoujia.com/apps/',\
            'http://www.wandoujia.com/top/app',\
            'http://www.wandoujia.com/top/game',\
            'http://www.wandoujia.com/tag/game'
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            #re.compile(r'http://www\.wandoujia\.com/apps/.+'),\
                            re.compile(r'http://www\.wandoujia\.com/tag/.+')\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://www\.wandoujia\.com/apps/.+'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='app-info']/p[@class='app-name']/span/text()").extract())
        size = ''.join(sel.xpath("//dl[@class='infos-list']/dd[1]/text()").extract())
        url = ''.join(sel.xpath("//div[@class='download-wp']/a[1]/@href").extract())
        size = size.strip()

        item['name'] = name
        item['url'] = url
        item['size'] = size

        #print '[-]', 'name: ', name.encode('utf-8'), 'url: ', url, 'size: ', size
        time.sleep(5)
        return item

