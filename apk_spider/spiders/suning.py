#coding:utf-8
import scrapy
from apk_spider.items import APKItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import tools
import time

class _SuningApkSpider(CrawlSpider):
    name = 'suning'
    allowed_domains = ['app.suning.com']
    start_urls = [\
            'http://app.suning.com/android',\
            ]

    rules = (\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://app\.suning\.com/android/app\?gid.+'),\
                        ),\
                    )\
                ),\
                Rule(\
                    LinkExtractor(\
                        allow=(\
                            re.compile(r'http://app\.suning\.com/android/app/page\?pack.+'),\
                        )\
                    ),\
                    callback='parse_item'\
                ),\
            )

    def parse_item(self,response):
        item = APKItem()
        sel = Selector(response)
        name = ''.join(sel.xpath("//div[@class='clearfix']/dl[@class='detail-top fl']/dd/h3/text()").extract())
        size = ''.join(sel.xpath("//div[@class='detail-con clearfix']/dl[@class='detail-main clearfix']/dd[1]/p[1]/span/text()").extract())
        url = ''.join(sel.xpath("//div[@class='app-dlbtn']/span[@class='dl2pc']/a/@href").extract())
        size = size.strip()

        item['name'] = name
        item['url'] = url
        item['size'] = size

        #print '[-]', 'name: ', item['name'].encode('utf-8'), 'url: ', item['url'], 'size: ', item['size']
        time.sleep(5)
        return item

