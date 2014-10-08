# -*- coding:utf-8 -*-
import os

TMP_DIR=r'apk_spider/tmp'

def kill_all_spiders():
        command = 'pkill -9 scrapy'
        os.system(command)

if __name__=='__main__':
    kill_all_spiders()
