# -*- encoding:utf8 -*-

import json
import urllib
import urllib2
import mongodb
import time
import sys
import os
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

APIKEY = cf.get("scan_read", "apikey")
URL = cf.get("scan_read", "url")
INTERVAl = int(cf.get("scan_read", "interval"), 10)
BUF_LIMIT = int(cf.get("scan_read", "buf_limit"), 10)
LOG_NAME = cf.get("scan_read", "log_file")
LOG_FILE = os.path.join(LOG_PATH, LOG_NAME)

logger = set_logger("scan_read", LOG_FILE)
logger.info("@====scan_read start work.")

def get_file_md5():
    res = []
    db = mongodb.connect_readonly()
    if not db:
        logger.critical("DB error. Exit.")
        sys.exit(1)
    collection = db.file_info_list
    cur = collection.find(
            {"scan_status":"success", "type_tag":"none"},
            {"_id":0})
    length = cur.count()

    if not length:
        cur = collection.find(
                {"scan_status":"success", "type_tag":"retry"},
                {"_id":0}
                )
        length = cur.count()

    if length < BUF_LIMIT:
        pass
    else:
        length = BUF_LIMIT
    for i in range(length):
        res.append(cur.next())

    return res

def read_res(md5):
    parameters = {"resource": md5, "apikey": APIKEY}
    data = urllib.urlencode(parameters)
    req = urllib2.Request(URL, data)
    response = urllib2.urlopen(req)
    res = response.read()
    try:
        res_dict = json.loads(res)
    except Exception, e:
        logger.error(e)
        logger.info(res)
        return False

    if res_dict["response_code"] == 1:
        if res_dict["positives"] > 0:
            return "positive"
        else:
            return "negative"
    elif res_dict["response_code"] == -2:
        return "retry"

    logger.info(res)
    return False

def set_file_type(md5, res):
    db = mongodb.connect_readwrite()
    collection = db.file_info_list
    collection.update({"md5":md5}, {"$set":{"type_tag":res}})

def main():
    while True:
        file_md5_list = get_file_md5()
        if not file_md5_list:
            time.sleep(1)
            continue
        else:
            for i in file_md5_list:
                logger.info("+----------+")
                res = read_res(i["md5"])
                logger.info("%s: %s" %(i["md5"], res))
                if not res:
                    set_file_type(i["md5"], "fail")
                else:
                    set_file_type(i["md5"], res)

                logger.info("wait for %ds ..." %(INTERVAl))
                time.sleep(INTERVAl)


if __name__ == "__main__":
    logger.info("Welcome to Reader")
    main()

