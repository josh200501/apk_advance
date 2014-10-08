#!/usr/bin/env python
#encoding:utf8

import sys
import mongodb
import time
import os
import shutil
import ConfigParser
from tools import set_logger
from get_env import get_env_para


CFG_PATH, STORE_PATH, LOG_PATH = get_env_para()
RELEASE = True

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

MAL_NAME = cf.get("store", "mal_folder")
NOR_NAME = cf.get("store", "nor_folder")
BUF_LIMIT = cf.get("store", "buf_limit")
LOG_NAME = cf.get("store", "log_file")
LOG_FILE = os.path.join(LOG_PATH, LOG_NAME)

MAL_FOLDER = os.path.join(STORE_PATH, MAL_NAME)
NOR_FOLDER = os.path.join(STORE_PATH, NOR_NAME)

logger = set_logger("store", LOG_FILE)
logger.info("@====store start work.")

def get_file_list():
    res = []
    db = mongodb.connect_readonly()
    if not db:
        logger.critical("DB error. Exit.")
        sys.exit(1)
    collection = db.file_info_list
    cur = collection.find(
            {"archive_flag":"none", "type_tag":{"$ne":"none"}},
            {"_id":0})
    length = cur.count()
    if length < BUF_LIMIT:
        pass
    else:
        length = BUF_LIMIT
    for i in range(length):
        try:
            res.append(cur.next())
        except:
            logger.error("error on read file from database.")
            break
    return res

def del_file(file_path):
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            logger.info("removed {0}".format(file_path))
            return True
        except:
            logger.error("fail to remove {0}".format(file_path))
            return False
    else:
        logger.error("{0} not exist.".format(file_path))
        return False

def move_file(name, src_path, dst_path, md5):
    src_name = name
    dst_name = name
    if not os.path.exists(dst_path):
        try:
            os.makedirs(dst_path)
        except:
            logger.critical("Fail to create dst path.")
            sys.exit(1)
    os.chdir(dst_path)
    while os.path.isfile(dst_name):
        dst_name = dst_name + "1"

    src_path_full = os.path.join(src_path, src_name)
    dst_path_full = os.path.join(dst_path, dst_name)
    try:
        shutil.move(src_path_full, dst_path_full)
        logger.info("%s -> %s" %(src_path_full, dst_path_full))
        return True
    except Exception, e:
        logger.error(str(e))
        return False

def set_file_archive_flag(md5, archive_flag):
    db = mongodb.connect_readwrite()
    if not db:
        logger.critical("DB error. exit.")
        sys.exit(1)

    collection = db.file_info_list
    collection.update({"md5":md5}, {"$set":{"archive_flag":archive_flag}}, multi=True)

def main():
    while True:
        time.sleep(1)
        file_list = get_file_list()
        if not file_list:
            time.sleep(1)
            continue
        else:
            for i in file_list:
                if not "name" in i.keys() or not "date" in i.keys():
                    continue
                index = i["name"].rindex("/")
                tmp = i["date"].split("-")
                date = tmp[0]

                name = i["name"][index+1:]
                src_path = i["name"][:index]
                if i["type_tag"] == "positive":
                    TYPE_FD = MAL_FOLDER
                elif i["type_tag"] == "negative":
                    TYPE_FD = NOR_FOLDER
                else:
                    continue
                dst_path = os.path.join(TYPE_FD, date)
                if RELEASE:
                    if i["type_tag"] == "negative":
                        res = del_file(i["name"])
                    else:
                        res = move_file(name, src_path, dst_path, i["md5"])
                else:
                    res = move_file(name, src_path, dst_path, i["md5"])
                if not res:
                    set_file_archive_flag(i["md5"], "fail")
                else:
                    set_file_archive_flag(i["md5"], "success")

if __name__ == "__main__":
    pid = os.getpid()
    PID_FILE = os.path.join(LOG_PATH, "pidfile")
    fp = open(PID_FILE, "a")
    fp.write(str(pid)+os.linesep)
    fp.close()

    main()

