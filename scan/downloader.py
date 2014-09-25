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

COUNTER = 0

mutex = threading.Lock()

DL_INIT_STATUS = "wait"

CFG = "../config.ini"
STORE = "../store"
LOG = "../log"

STORE_PATH = os.path.join(os.getcwd(), STORE)
LOG_PATH = os.path.join(os.getcwd(), LOG)

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

cf_path = os.path.join(os.getcwd(), CFG)
if not os.path.isfile(cf_path):
    print "no config.ini"
    sys.exit(1)
cf = ConfigParser.ConfigParser()
cf.read(cf_path)

BUF_LIMIT = int(cf.get("downloader", "buf_limit"), 10)
SIZE_LIMIT = int(cf.get("downloader", "size_limit"), 10)
RETRY_TIME = cf.get("downloader", "retry_time")
TMP_NAME = cf.get("downloader", "tmp_path")
LOG_NAME = cf.get("downloader", "log_file")
CONCURRENT = int(cf.get("downloader", "concurrent"))

TMP_FOLDER = os.path.join(STORE_PATH, TMP_NAME)
LOG_FILE = os.path.join(LOG_PATH, LOG_NAME)

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
        res.append(cur.next())

    return res

def del_tmpfile(fp):
    if os.path.isfile(fp):
        try:
            os.remove(fp)
        except Exception, e:
            logger.error(e)
    else:
        pass

def get_file(url):
    file_info = {}
    file_name = str(time.time()) + ".apk"
    file_path = os.path.join(TMP_FOLDER, file_name)
    try:
        os.chdir(TMP_FOLDER)
        res_code = os.system("wget --tries=%s -O  %s %s"
                %(RETRY_TIME, file_name, url))
        if res_code:
            return False
        ft = get_file_type(file_path)
        if "HTML" in ft:
            del_tmpfile(file_path)
            return False

        file_info["name"] = file_path
        md5 = tools.md5sum(file_path)
        if not md5:
            del_tmpfile(file_path)
            return False
        if check_dup(md5):
            del_tmpfile(file_path)
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
        logger.error(e)
        return False

    return file_info

def url_handler(url):
    logger.info("Download start: %s" %(url))
    set_url_status(url, "start")
    file_info = get_file(url)
    if not file_info:
        logger.info("Download fail: %s" %(url))
        set_url_status(url, "fail")
    else:
        logger.info("Download success: %s" %(url))
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
    collection = db.apk_url_download_candidate_list
    collection.update({"url":url}, {"$set":{"download_status":status}})

def set_file_info(file_information):
    db = mongodb.connect_readwrite()
    collection = db.file_info_list
    collection.insert(file_information)

def check_dup(md5):
    db = mongodb.connect_readwrite()
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

        if fs_num > SIZE_LIMIT:
            return False
        else:
            return True

    elif "KB" in file_size:
        return True
    else:
        return False

def main():
    while True:
        urls = get_apk_url()
        if not urls:
            time.sleep(1)
            continue

        while True:
            i = urls[0]
            if "size" not in i.keys():
                set_url_status(i["url"], "size_error")
                del urls[0]
                continue
            if not check_size(i["size"]):
                set_url_status(i["url"], "size_error")
                del urls[0]
                continue

            global COUNTER
            if COUNTER < CONCURRENT:
                if mutex.acquire(1):
                    COUNTER = COUNTER + 1
                mutex.release()
                uh = UrlHandler(i["url"])
                uh.start()
                del urls[0]
                if not urls:
                    break
            else:
                time.sleep(0.5)

if __name__ == '__main__':
    logger.info("Welcome to downloader!")
    main()

