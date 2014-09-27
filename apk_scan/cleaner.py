#!/usr/bin/env python
# endcoding:utf8

import mongodb
import time
import os
import sys
import ConfigParser
from tools import set_logger
from tools import md5sum
from get_env import get_env_para


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
LOG_NAME = cf.get("cleaner", "log_file")

TMP_FOLDER = os.path.join(STORE_PATH, TMP_NAME)
LOG_FILE = os.path.join(LOG_PATH, LOG_NAME)

logger = set_logger("cleaner", LOG_FILE)
logger.info("@=====cleaner start work.")

if not os.path.exists(TMP_FOLDER):
    logger.warn("%s: not exist." %(TMP_FOLDER))
    try:
        logger.info("Try to create: %s." %(TMP_FOLDER))
        os.makedirs(TMP_FOLDER)
    except:
        logger.critical("Fail to create temp directory. Exit.")
        sys.exit(1)

def walk_dir(root_path):
    length = len(root_path)
    file_list = []
    list_dir = os.walk(root_path)
    for root, dirs, files in list_dir:
        for f in files:
            file_list.append(os.path.join(root, f))

    return file_list

def check_db(md5):
    db = mongodb.connect_readwrite()
    if not db:
        logger.critical("DB error. Exit.")
        sys.exit(1)

    collection = db.file_info_list
    cur = collection.find({"md5": md5})
    length = cur.count()
    if not length:
        return False
    else:
        return True

def del_file(file_path):
    if not os.path.isfile(file_path):
        logger.error("{0} not exist.".format(file_path))
        return False
    else:
        try:
            os.remove(file_path)
        except:
            logger.error("fail to remove {0}".format(file_path))
            return False
    return True

def main():
    count_all = 0
    count_notfound = 0
    file_list = walk_dir(TMP_FOLDER)
    count_all = len(file_list)
    for i in file_list:
        md5 = md5sum(i)
        if not check_db(md5):
            count_notfound += 1
            logger.info("not found {0} in db".format(i))
            continue

    logger.info("ALL: {0}, NOTFOUND: {1}".format(count_all, count_notfound, ))


if __name__ == '__main__':
    main()

