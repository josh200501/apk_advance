#!/usr/bin/env python
# endcoding:utf8

import urllib
import mongodb
import time
import os
import sys
import tools
import magic
import ConfigParser
from tools import set_logger
from tools import md5sum
import threading
from get_env import get_env_para
import subprocess


CFG_PATH, STORE_PATH, LOG_PATH = get_env_para()

if not os.path.exists(STORE_PATH):
    try:
        os.mkdir(STORE_PATH)
    except:
        print "fail to create: %s" %(STORE_PATH)
        sys.exit(1)

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

TMP_NAME = cf.get("downloader", "tmp_path")
LOG_NAME = cf.get("misc", "log_file")

TMP_FOLDER = os.path.join(STORE_PATH, TMP_NAME)
LOG_FILE = os.path.join(LOG_PATH, LOG_NAME)

logger = set_logger("check cons", LOG_FILE)
logger.info("@=====check cons start work.")

if not os.path.exists(TMP_FOLDER):
    logger.warn("%s: not exist." %(TMP_FOLDER))
    try:
        logger.info("Try to create: %s." %(TMP_FOLDER))
        os.makedirs(TMP_FOLDER)
    except:
        logger.critical("Fail to create temp directory. Exit.")
        sys.exit(1)


def get_file_list():
    res = []
    db = mongodb.connect_readwrite()
    if not db:
        logger.critical("DB error. Exit.")
        sys.exit(1)

    collection = db.file_info_list
    cur = collection.find()
    length = cur.count()
    for i in range(length):
        res.append(cur.next())
    return res

def check_cons():
    count_all = 0
    count_notfound = 0
    count_uncons = 0
    file_list = get_file_list()
    count_all = len(file_list)
    for i in file_list:
        if not "md5" in i.keys() or not "name" in i.keys():
            logger.warning("unexpected file: {0}".format(i))
            continue
        md5_db = i["md5"]
        file_path = i["name"]
        md5_local = md5sum(file_path)
        if not os.path.isfile(file_path):
            logger.error("{0} not exist.".format(file_path))
            count_notfound += 1
        if md5_db != md5_local:
            logger.error("{0} unconsistent.".format(file_path))
            count_uncons += 1
            continue

    logger.info("ALL: {0}, NOTFOUND: {1}, UNCONS: {2}".format(count_all, count_notfound, count_uncons))

def main():
    check_cons()

if __name__ == '__main__':
    main()

