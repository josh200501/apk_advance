#!/usr/bin/env python
#encoding:utf8

import os
import time
import sys
import subprocess
import colors
from get_env import get_env_para
from tools import set_logger

LOW_LIMIT = 6000
HIGH_LIMIT = 7000

CFG_PATH, STORE_PATH, LOG_PATH = get_env_para()

if not os.path.exists(LOG_PATH):
    try:
        os.mkdir(LOG_PATH)
    except:
        print colors.red("fail to create: %s" %(LOG_PATH))
        sys.exit(1)

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
        print "no statvfs supported. exit."
        sys.exit(1)

def stop_downloader():
    fp = open(PID_FILE)
    pids = fp.readlines()
    fp.close()
    for i in pids:
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
        print "kill process: {0}".format(pid_id)

def start_downloader():
    subprocess.Popen("downloader.py")

def write_pid():
    global PID_FILE
    pid = os.getpid()
    fp = open(PID_FILE, "a")
    fp.write(str(pid)+os.linesep)
    fp.close()

def monitor():
    global STORE_PATH
    run_path = STORE_PATH
    shutdown_flag = False
    while True:
        num, unit = get_freespace(run_path)
        print "freespace: {0}{1}".format(num, unit)
        if num < LOW_LIMIT and not shutdown_flag:
            shutdown_flag = True
            logger.info("freespace: {0}{1}".format(num, unit))
            logger.info("freespace becoming low, try to stop downloader ...")
            stop_downloader()
        elif num > HIGH_LIMIT and shutdown_flag:
            shutdown_flag = False
            logger.info("freespace is ok, start downloader again ...")
            start_downloader()
        time.sleep(5)

if __name__ == "__main__":
    write_pid()
    monitor()

