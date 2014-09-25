# -*- encoding: utf8 -*-

import postfile
import json
import mongodb
import sys
import time
import os
from scan_read import read_res
import ConfigParser
from tools import set_logger

CFG = "../config.ini"
LOG = "../log"

LOG_PATH = os.path.join(os.getcwd(), LOG)

if not os.path.exists(LOG_PATH):
    try:
        os.mkdir(LOG_PATH)
    except:
        print "fail to create: %s" %(LOG_PATH)
        sys.exit(1)

cf_path = os.path.join(os.getcwd(), CFG)
if not os.path.isfile(cf_path):
    print "no config.ini"
    sys.exit(1)
cf = ConfigParser.ConfigParser()
cf.read(cf_path)

APIKEY = cf.get("scan_upload", "apikey")
HOST = cf.get("scan_upload", "host")
SELECTOR = cf.get("scan_upload", "selector")
FIELDS = [("apikey",APIKEY)]

INTERVAl = int(cf.get("scan_upload", "interval"), 10)
BUF_LIMIT = int(cf.get("scan_upload", "buf_limit"), 10)

LOG_NAME = cf.get("scan_upload", "log_file")
LOG_FILE = os.path.join(LOG_PATH, LOG_NAME)

logger = set_logger("scan_upload", LOG_FILE)
logger.info("@====scan_upload start work.")

SIZE = 30

def get_file_list():
    res = []
    db = mongodb.connect_readonly()
    if not db:
        logger.error("DB error. Exit.")
        sys.exit(1)
    collection = db.file_info_list
    cur = collection.find({"scan_status":"none"}, {"_id":0})
    length = cur.count()
    if length < BUF_LIMIT:
        pass
    else:
        length = BUF_LIMIT
    for i in range(length):
        res.append(cur.next())

    return res

def scan(file_path, md5):
    if read_res(md5):
        return True

    file_size = os.path.getsize(file_path)
    if file_size > SIZE*1024*1024:
        logger.error("File too large.")
        return False
    file_to_send = open(file_path, "rb").read()
    files = [("file", "test", file_to_send)]
    res = postfile.post_multipart(HOST, SELECTOR, FIELDS, files)
    logger.info(res)
    try:
        res = json.loads(res)
    except Exception, e:
        logger.error(e)
        return False
    if res["response_code"] == 1:
        return True
    else:
        return False

def set_file_scan_status(md5, status):
    db = mongodb.connect_readwrite()
    collection = db.file_info_list
    collection.update({"md5":md5},{"$set":{"scan_status":status}})

def main():
    while True:
        files = get_file_list()
        if not files:
            time.sleep(1)
            continue
        else:
            for i in files:
                logger.info("+----------+")
                logger.info("Scan: %s" %(i["name"]))
                if not scan(i["name"], i["md5"]):
                    set_file_scan_status(i["md5"], "fail")
                    logger.info("%s upload fail." %(i["name"]))
                else:
                    set_file_scan_status(i["md5"], "success")
                    logger.info("%s upload success." %(i["name"]))

                logger.info("wait for %ds ..." %(INTERVAl))
                time.sleep(INTERVAl)

if __name__ == "__main__":
    logger.info("Welcome to Scaner")
    main()

