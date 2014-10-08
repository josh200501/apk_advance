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
DB_READ_USER = cf.get('mongodb','read_user')
DB_READ_PASSWORD = cf.get('mongodb','read_password')
g_logger = tools.set_logger('spider_mongo',os.path.join(os.getcwd()+'/log/',cf.get('spider','log_path')))

def connect_readwrite():
    try:
       con = pymongo.Connection(DB_ADDR,DB_PORT)
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
    url = ''.join(item['url'])
    name = ''.join(item['name'])
    size = ''.join(item['size'])
    urlhash = tools.sha1(url)
    insert_time = tools.get_current_time()
    status = 'wait'
    db = connect_readwrite()
    collection = db.apk_url_download_candidate_list
    if size == '':
        collection.insert({'url':url,'url_hash':urlhash,'worker_id':workerid,'download_status':status,'name':name,'size':'-1MB','time':insert_time})
    else:
        collection.insert({'url':url,'url_hash':urlhash,'worker_id':workerid,'download_status':status,'name':name,'size':size,'time':insert_time})
#        g_logger.info('Insert %s.' % url)

def batch_insert_to_download_candidate_list(item_list,workerid):
    item_list2 = []
    for item in item_list:
        url = ''.join(item['url'])
        name = ''.join(item['name'])
        size = ''.join(item['size'])
        urlhash = tools.sha1(url)
        status = 'wait'
        insert_time = tools.get_current_time()
        if size == '':
            size = '-1MB'
        item_list2.append({'url':url,'url_hash':urlhash,'worker_id':workerid,'download_status':status,'name':name,'size':size,'time':insert_time})
    db = connect_readwrite()
    collection = db.apk_url_download_candidate_list
    collection.insert(item_list2)

def is_url_exist(url):
    db = connect_readwrite()
    collection = db.apk_url_download_candidate_list
    if collection.find_one({'url':url}) != None:
        return True
    return False

def connect_mutex():
    try:
       con = pymongo.Connection(DB_ADDR,DB_PORT)
       db = con.mutex
       db.authenticate('apk_mutex','apk_mutex')
       g_logger.info('Database mutex connected.')
    except:
        traceback.print_exc()
        g_logger.critical('Databse mutex connect error,exit.')
    return db

def set_collection_using():
    db = connect_mutex()
    collection = db.mutex_apk_url_download_candidate_list
    result = collection.findAndModify({query:{'using':False},update:{'using':True}})
    if result == None:
        return False
    return True

def set_collection_free():
    db = connect_mutex()
    collection = db.mutex_apk_url_download_candidate_list
    collection.findAndModify({query:{'using':True},update:{'using':False}})

