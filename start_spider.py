# -*- coding:utf-8 -*-
import os

TMP_DIR=r'apk_spider/tmp'

def start_all_spiders():
    spiders = os.popen('scrapy list').readlines()
    if os.path.exists(TMP_DIR):
        pass
    else:
        os.mkdir(TMP_DIR)
    for spider in spiders:
        spider = spider.rstrip('\n')
        command = 'scrapy crawl '+spider+' -s JOBDIR='+TMP_DIR+'/'+spider
        os.system(command+' &')

if __name__=='__main__':
    start_all_spiders()
