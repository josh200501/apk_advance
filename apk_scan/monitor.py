#!/usr/bin/env python
#encoding:utf8

import os
import time
import sys
import subprocess
import colors
from get_env import get_env_para
from tools import set_logger
import ConfigParser


CFG_PATH, STORE_PATH, LOG_PATH = get_env_para()

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

DISK_LOW_LIMIT = int(cf.get("disk", "low_limit"), 10)
DISK_RSD_LIMIT = int(cf.get("disk", "rsd_limit"), 10)

PID_FILE = os.path.join(LOG_PATH, "pidfile")
LOG_FILE = os.path.join(LOG_PATH, "monitor.log")

logger = set_logger("monitor", LOG_FILE)
logger.info("@=====monitor start work.")

def get_freespace(dir_path):
    space_avaliable = 0
    if hasattr(os, "statvfs"):
        dir_status = os.statvfs(dir_path)
        space_avaliable = dir_status.f_bavail * dir_status.f_frsize
        space_avaliable /= 1024 * 1024
        return (space_avaliable, "MB")
    else:
        logger.critical("no statvfs supported. exit.")
        sys.exit(1)

def stop_downloader():
    flag = False
    try:
        fp = open(PID_FILE)
        pids = fp.readlines()
    except Exception, e:
        logger.error(str(e))
        return
    finally:
        fp.close()
    #logger.info("read pidfile: ok")
    #logger.info("total itemus: {0}".format(len(pids)))
    for i in pids:
        logger.info("processing {0}".format(i))
        i = i.strip()
        if not i:
            continue
        pid = i.split("-")
        if len(pid) < 2:
            continue
        else:
            if pid[0] == "downloader":
                pid_id = pid[1]
            else:
                continue
        subprocess.call(["kill", "-9", pid_id])
        logger.info("kill process: {0}".format(pid_id))
        flag = True

    if flag:
        return True
    logger.info("do not found downloader process")
    return False

def start_downloader():
    exec_path = os.getcwd()
    abs_exec_path = os.path.join(exec_path, "downloader.py")
    os.chdir(exec_path)
    try:
        subprocess.Popen(["python",abs_exec_path])
        return True
    except Exception, e:
        logger.error(str(e))
        return False

def write_pid():
    global PID_FILE
    pid = os.getpid()
    try:
        fp = open(PID_FILE, "a")
        fp.write(str(pid)+os.linesep)
    except Exception, e:
        logger.critical(str(e))
        sys.exit(1)
    finally:
        fp.close()

def stop():
    fp = open(PID_FILE)
    pids = fp.readlines()
    fp.close()
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    os.chdir(parent_dir)
    subprocess.Popen(["python", "kill_spider.py"])
    for i in pids:
        i = i.strip()
        if not i:
            continue
        pid = i.split("-")
        if len(pid) < 2:
            pid_id = pid[0]
        else:
            pid_id = pid[1]
        subprocess.call(["kill", "-9", pid_id])
        logger.info("kill process: {0}".format(pid_id))

def monitor():
    global STORE_PATH
    run_path = STORE_PATH
    shutdown_flag = False
    while True:
        num, unit = get_freespace(run_path)
        print "freespace: {0}{1}".format(num, unit)
        if num < DISK_LOW_LIMIT and not shutdown_flag:
            shutdown_flag = True
            logger.info("freespace: {0}{1}".format(num, unit))
            logger.info("freespace becoming low, try to stop downloader ...")
            while not stop_downloader():
                time.sleep(3)
                logger.info("try to stop downloader ...")
        elif num > DISK_RSD_LIMIT and shutdown_flag:
            shutdown_flag = False
            logger.info("freespace: {0}{1}".format(num, unit))
            logger.info("freespace is ok, start downloader again ...")
            while not start_downloader():
                time.sleep(3)
                logger.info("try to start downloader ...")
        time.sleep(5)

if __name__ == "__main__":
    write_pid()
    while True:
        try:
            monitor()
        except Exception, e:
            logger.error(str(e))
            time.sleep(3)
            continue


