#!/usr/bin/env python
#encoding:utf8

import os
import time
import sys
import subprocess

LOW_LIMIT = 3500
LOW_LIMIT = 8500
HIGH_LIMIT = 5000

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

if __name__ == "__main__":
    pid = os.getpid()
    cwd = os.getcwd()
    PID_FILE = os.path.join(cwd, "log/pidfile")
    fp = open(PID_FILE, "a")
    fp.write(str(pid)+os.linesep)
    fp.close()

    path = "/"
    shutdown_flag = False
    while True:
        time.sleep(10)
        num, unit = get_freespace(path)
        if num < LOW_LIMIT and not shutdown_flag:
            shutdown_flag = True
            print "freespace: {0}{1}".format(num, unit)
            print "freespace becoming low ..."
            print "try to shutdown downloader..."
            os.chdir(os.getcwd())
            subprocess.call([os.path.join(cwd, "sys_control.py"),
                    "stop_downloader"])
        elif num > HIGH_LIMIT and shutdown_flag:
            shutdown_flag = False
            os.chdir(os.path.join(cwd, "apk_scan/"))
            subprocess.Popen([os.path.join(cwd, "apk_scan/downloader.py")])

