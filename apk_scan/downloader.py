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
import threading
from get_env import get_env_para
import subprocess
import colors

COUNTER = 0

mutex = threading.Lock()

DL_INIT_STATUS = "wait"


CFG_PATH, STORE_PATH, LOG_PATH = get_env_para()

if not os.path.exists(STORE_PATH):
    try:
        os.mkdir(STORE_PATH)
    except:
        print colors.red("fail to create: %s" %(STORE_PATH))
        sys.exit(1)

if not os.path.exists(LOG_PATH):
    try:
        os.mkdir(LOG_PATH)
    except:
        print colors.red("fail to create: %s" %(LOG_PATH))
        sys.exit(1)

if not os.path.isfile(CFG_PATH):
    print colors.red("no config.ini")
    sys.exit(1)
cf = ConfigParser.ConfigParser()
cf.read(CFG_PATH)

BUF_LIMIT = int(cf.get("downloader", "buf_limit"), 10)
SIZE_LIMIT = int(cf.get("downloader", "size_limit"), 10)
RETRY_TIME = cf.get("downloader", "retry_time")
TMP_NAME = cf.get("downloader", "tmp_path")
LOG_NAME = cf.get("downloader", "log_file")
CONCURRENT = int(cf.get("downloader", "concurrent"))

TMP_FOLDER = os.path.join(STORE_PATH, TMP_NAME)
LOG_FILE = os.path.join(LOG_PATH, LOG_NAME)

PID_FILE = os.path.join(LOG_PATH, "pidfile")

logger = set_logger("downloader", LOG_FILE)
logger.info("@=====Downloader start work.")

if not os.path.exists(TMP_FOLDER):
    logger.warn("%s: not exist." %(TMP_FOLDER))
    try:
        logger.info("Try to create: %s." %(TMP_FOLDER))
        os.makedirs(TMP_FOLDER)
    except:
        logger.critical("Fail to create temp directory. Exit.")
        sys.exit(1)



class UrlHandler(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        url_handler(self.url)

def get_apk_url():
    res = []
    db = mongodb.connect_readonly()
    if not db:
        logger.critical("DB error. Exit.")
        sys.exit(1)
    collection = db.apk_url_download_candidate_list
    cur = collection.find(
            {"download_status":DL_INIT_STATUS},
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
            logger.error("error on read url.")
            break
    return res

def del_tmpfile(fp):
    if os.path.isfile(fp):
        try:
            os.remove(fp)
            return True
        except Exception, e:
            logger.error(str(e))
            return False
    else:
        logger.error("%s not exist." %(fp))
        return False

def get_file(url):
    file_info = {}

    if mutex.acquire(1):
        time_stamp = time.time()
    mutex.release()

    file_name = str(long(time_stamp * 1000000)) + ".apk"
    file_path = os.path.join(TMP_FOLDER, file_name)
    try:
        os.chdir(TMP_FOLDER)

        """"
        res_code = subprocess.call("wget --tries=%s -O  %s %s"
                %(RETRY_TIME, file_name, url))
        """

        res_code = subprocess.call(["wget", "--tries={0}".format(RETRY_TIME),
                "-nv", "-O", file_name, url])

        if res_code:
            del_tmpfile(file_path)
            logger.error("wget res code: {0}".format(res_code))
            return False
        # in case wget have not create file because of the function of buffer
        while not os.path.isfile(file_path):
            time.sleep(0.1)
        ft = get_file_type(file_path)
        if not ft:
            del_tmpfile(file_path)
            logger.error("fail to get file type")
            return False

        if not "Java" in ft and not "Zip" in ft:
            del_tmpfile(file_path)
            logger.error("file type not match:%s -> %s" %(file_path, ft))
            return False

        file_info["name"] = file_path
        md5 = tools.md5sum(file_path)
        if not md5:
            del_tmpfile(file_path)
            logger.error("fail to get file md5")
            return False
        if check_dup(md5):
            del_tmpfile(file_path)
            logger.error("file dup: %s -- %s" %(file_path, md5))
            return False

        file_info["md5"] = md5
        file_info["url"] = url
        file_info["date"] = time.strftime(
                "%Y%m%d-%H:%M:%S",
                time.localtime())
        file_info["type_tag"] = "none"
        file_info["scan_status"] = "none"
        file_info["archive_flag"] = "none"
    except Exception, e:
        logger.error(str(e))
        return False

    return file_info

def url_handler(url):
    #logger.info("Download start: %s" %(url))
    file_info = get_file(url)
    if not file_info:
        logger.info(colors.red("Download fail: %s" %(url)))
        set_url_status(url, "fail")
    else:
        logger.info(colors.green("Download success: %s" %(url)))
        set_url_status(url, "success")
        set_file_info(file_info)
    global COUNTER
    if mutex.acquire(1):
        COUNTER = COUNTER - 1
    mutex.release()

def get_file_type(file_path):
    file_type = ""
    try:
        if sys.platform.startswith("linux"):
            file_type = magic.from_file(file_path)
        else:
            logger.critical("not support this platform.")
            sys.exit(1)
    except Exception, e:
        logger.error(e)

    return file_type

def set_url_status(url, status):
    db = mongodb.connect_readwrite()
    if not db:
        logger.critical("DB error. Exit.")
        sys.exit(1)

    collection = db.apk_url_download_candidate_list
    collection.update({"url":url}, {"$set":{"download_status":status}}, multi=True)

def set_file_info(file_information):
    db = mongodb.connect_readwrite()
    if not db:
        logger.critical("DB error. Exit.")
        sys.exit(1)

    collection = db.file_info_list
    collection.insert(file_information)

def check_dup(md5):
    db = mongodb.connect_readwrite()
    if not db:
        logger.critical("DB error. Exit.")
        sys.exit(1)

    collection = db.file_info_list
    collection.update({"md5":md5}, {"$set":{"md5":md5}})
    res = db.command({"getLastError": 1})
    if res["updatedExisting"]:
        return True
    else:
        return False

def check_size(file_size):

    if "MB" in file_size:
        fs_num = file_size.split(".")[0]

        if "MB" in fs_num:
            fs_num = file_size[:file_size.rindex("MB")]

        try:
            fs_num = int(fs_num, 10)
        except:
            logger.error("fail to convert str to int.")
            return False

        if fs_num > SIZE_LIMIT or fs_num <= 0:
            return False
        else:
            return True

    elif "KB" in file_size:
        return True
    else:
        return False

def main():
    idle_flag = False
    while True:
        urls = get_apk_url()
        if not urls:
            st = 5
            #print "wait for %ds ..." %(st)
            time.sleep(st)
            if not idle_flag:
                logger.info("nothing to do.")
                idle_flag = True
            continue
        idle_flag = False
        while True:
            #print "to download: ", len(urls)
            i = urls[0]
            if "size" not in i.keys():
                logger.warning("{0} size error".format(i["url"]))
                set_url_status(i["url"], "size_error")
                del urls[0]
                if not urls:
                    break
                else:
                    continue

            if not check_size(i["size"]):
                logger.warning("{0} size error".format(i["url"]))
                set_url_status(i["url"], "size_error")
                del urls[0]
                if not urls:
                    break
                else:
                    continue

            global COUNTER
            if COUNTER < CONCURRENT:
                if mutex.acquire(1):
                    COUNTER = COUNTER + 1
                mutex.release()
                set_url_status(i["url"], "start")
                uh = UrlHandler(i["url"])
                uh.start()
                del urls[0]
                if not urls:
                    break
            else:
                time.sleep(1)

def write_pid():
    global PID_FILE
    pid = os.getpid()
    try:
        fp = open(PID_FILE, "a")
        fp.write("downloader"+"-"+str(pid)+os.linesep)
    except Exception, e:
        logger.critical(str(e))
        sys.exit(1)
    finally:
        fp.close()

if __name__ == '__main__':
    write_pid()
    try:
        main()
    except Exception, e:
        logger.error(str(e))

