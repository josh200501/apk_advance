#!/usr/bin/env python
#encoding:utf8

import json
import urllib
import urllib2
import mongodb
import time
import sys
import os
import ConfigParser
from tools import set_logger
import postfile
from get_env import get_env_para


CFG_PATH, STORE_PATH, LOG_PATH = get_env_para()

if not os.path.exists(LOG_PATH):
    try:
        os.mkdir(LOG_PATH)
    except:
        print "fail to create: %s" %(LOG_PATH)
        sys.exit(1)

if not os.path.isfile(CFG_PATH):
    print "no config.ini"
    sys.exit(1)

cf = ConfigParser.ConfigParser()
cf.read(CFG_PATH)

APIKEY = cf.get("scanner", "apikey")
URL = cf.get("scanner", "url")
INTERVAl = int(cf.get("scanner", "interval"), 10)
BUF_LIMIT = int(cf.get("scanner", "buf_limit"), 10)
LOG_NAME = cf.get("scanner", "log_file")
LOG_FILE = os.path.join(LOG_PATH, LOG_NAME)

HOST = cf.get("scanner", "host")
SELECTOR = cf.get("scanner", "selector")
FIELDS = [("apikey",APIKEY)]

logger = set_logger("scanner", LOG_FILE)
logger.info("@====scanner start work.")

JUDGERS = ["Emsisoft", "ESET-NOD32", "Kaspersky", "Kingsoft"]

SIZE = 30
RESCAN = False

def get_file_list():
    global RESCAN
    res = []
    db = mongodb.connect_readonly()
    if not db:
        logger.critical("DB error. Exit.")
        sys.exit(1)
    collection = db.file_info_list
    cur = collection.find({"scan_status":"none"}, {"_id":0})
    length = cur.count()

    RESCAN = False
    if not length:
        RESCAN = True
        cur = collection.find(
                {"scan_status":"success", "type_tag":"none"},
                {"_id":0}
                )
        length = cur.count()

    if length < BUF_LIMIT:
        pass
    else:
        length = BUF_LIMIT
    for i in range(length):
        try:
            res.append(cur.next())
        except:
            logger.error("error on read file list from database.")
            break
    return res

def read_report(md5):
    parameters = {"resource": md5, "apikey": APIKEY}
    data = urllib.urlencode(parameters)
    req = urllib2.Request(URL, data)
    response = urllib2.urlopen(req)
    try:
        res = response.read()
    except Exception, e:
        logger.error("error on read response.")
        logger.error(str(e))
        return False
    logger.info("report response: {0} --> {1}".format(md5, res))
    return res

def scan(file_path, md5):
    file_size = os.path.getsize(file_path)
    if file_size > SIZE*1024*1024:
        logger.error("file too large: {0} --> {1} Bytes".format(
                file_path, file_size))
        return False
    file_to_send = open(file_path, "rb").read()
    files = [("file", "test", file_to_send)]
    try:
        res = postfile.post_multipart(HOST, SELECTOR, FIELDS, files)
    except Exception, e:
        logger.error("upload fail: {0}".format(file_path))
        logger.error(str(e))
        return False
    logger.info("scan response: {0} --> {1}".format(md5, res))
    return res

def set_file_scan_status(md5, status):
    db = mongodb.connect_readwrite()
    if not db:
        logger.critical("DB error, exit.")
        sys.exit(1)

    collection = db.file_info_list
    collection.update({"md5":md5},{"$set":{"scan_status":status}})

def set_file_type(md5, type_tag, type_res):
    db = mongodb.connect_readwrite()
    if not db:
        logger.critical("DB error, exit.")
        sys.exit(1)

    collection = db.file_info_list
    collection.update({"md5":md5}, {"$set":{"type_tag":type_tag}})
    collection.update({"md5":md5}, {"$set":{"type_res":type_res}})


def check_json(res):
    try:
        res_dict = json.loads(res)
    except Exception, e:
        logger.error("error on load josn data: {0}".format(e))
        return False
    return res_dict

def scan_online_virustotal(file_path, md5):
    md5_db = md5
    md5_scan = ""
    res_read = read_report(md5)
    if not res_read:
        logger.critical("fail to read response, network error.")
        sys.exit(1)

    res_read_dict = check_json(res_read)
    if not res_read_dict:
        logger.error("unknown error occur.")
        sys.exit(1)

    if res_read_dict["response_code"] == 1:
        md5_scan = res_read_dict["md5"]
        if md5_db != md5_scan:
            logger.error("file md5 was inconsistent: md5_db:{0} <> md5_scan:{1}".format(md5_db, md5_scan))
            sys.exit(1)
        type_tag, type_res = determine(res_read_dict)
        logger.info("scan res: {0}: {1} --> {2}".format(
                md5, type_tag, type_res))
        set_file_scan_status(md5, "success")
        set_file_type(md5, type_tag, type_res)
    else:
        if RESCAN:
            set_file_scan_status(md5, "fail")
            return False
        else:
            logger.info("wait for {0}s to upload file ... (api quota)".format(INTERVAl))
            time.sleep(INTERVAl)
            logger.info("start to upload: {0}".format(md5))
            res_scan = scan(file_path, md5)
            if not res_scan:
                logger.critical("fail to read scan response, network error.")
                sys.exit(1)
            else:
                res_scan_dict = check_json(res_scan)
                if not res_scan_dict:
                    logger.error("unknown error occur.")
                    sys.exit(1)
                # scan succed
                if res_scan_dict["response_code"] == 1:
                    md5_scan = res_scan_dict["md5"]
                    if md5_db != md5_scan:
                        logger.error("file md5 was inconsistent: md5_db:{0} <> md5_scan:{1}".format(
                                        md5_db, md5_scan))
                        sys.exit(1)

                    logger.info("upload success: {0}".format(md5))
                    set_file_scan_status(md5, "success")
                else:
                    logger.info("upload fail: {0}".format(md5))
                    set_file_scan_status(md5, "fail")

def determine(res):
    type_tag = "negative"
    type_res = ""
    if res["positives"] < 1:
        type_tag = "negative"
        return (type_tag, type_res)
    else:
        scanner = res["scans"]
        for i in JUDGERS:
            if i in scanner.keys():
                if scanner[i]["detected"]:
                    type_res = (i, scanner[i]["result"])
                    type_tag = "positive"
                    break
                else:
                    continue
    return (type_tag, type_res)

def main():
    while True:
        file_list = get_file_list()
        if not file_list:
            st = 3
            print "wait for {0} s".format(st)
            time.sleep(st)
            continue
        else:
            for i in file_list:
                logger.info("[+]==========[+]")
                md5 = i["md5"]
                fp = i["name"]
                scan_online_virustotal(fp, md5)
                logger.info("wait for {0}s to scan next ... (api quota)".format(INTERVAl))
                time.sleep(INTERVAl)

if __name__ == "__main__":
    main()

