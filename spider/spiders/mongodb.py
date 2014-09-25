#coding:utf-8
import os
import pymongo
import ConfigParser
import traceback
import tools
from apk_spider.items import APKItem

config_file = os.getcwd()+'/apk_spider/spiders/spider_config.ini'
cf = ConfigParser.ConfigParser()
cf.read(config_file)
DB_ADDR = cf.get('mongodb','addr')
DB_PORT = int(cf.get('mongodb','port'),10)
DB_READWRITE_USER = cf.get('mongodb','readwrite_user')
DB_READWRITE_PASSWD = cf.get('mongodb','readwrite_password')
g_logger = tools.set_logger('spider_mongo',os.path.join(os.getcwd()+'/log/',cf.get('spider','log_path')))

def connect_readwrite():
    try:
       con = pymongo.Connection(DB_ADDR,DB_PORT)
       #mydb is the database name
       db = con.mydb
       db.authenticate(DB_READWRITE_USER,DB_READWRITE_PASSWD)
       g_logger.info('Database connected.')
    except:
        traceback.print_exc()
        g_logger.critical('Databse connect error,exit.')
    return db

def insert_to_download_candidate_list2(url,urlhash,workerid,download_status,time):
    db = connect_readwrite()
    collection = db.apk_url_download_candidate_list
    collection.insert({'url':url,'url_hash':urlhash,'worker_id':workerid,'download_status':download_status,'time':time})

def insert_to_download_candidate_list(item,workerid):

#    for item in item_list:
    url = ''.join(item['url'])
    name = ''.join(item['name'])
    size = ''.join(item['size'])
#    if url == '':
#        return
#    if url[-3:] != 'apk':
#        return
    urlhash = tools.sha1(url)
    insert_time = tools.get_current_time()
    status = 'wait'
    db = connect_readwrite()
    collection = db.apk_url_download_candidate_list
    if size == '':
        collection.insert({'url':url,'url_hash':urlhash,'worker_id':workerid,'download_status':status,'name':name,'size':'0MB','time':insert_time})
    else:
        collection.insert({'url':url,'url_hash':urlhash,'worker_id':workerid,'download_status':status,'name':name,'size':size,'time':insert_time})
        g_logger.info('Insert %s.' % url)
