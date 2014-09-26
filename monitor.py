#!/usr/bin/env python
#encoding:utf8

import os
import time
import sys
import subprocess

LIMIT = 5 * 1024 * 1024

def get_freespace(dir_path):
    if hasattr(os, "statvfs"):
        dir_status = os.statvfs(dir_path)

        space_avaliable = dir_status.f_bavail * dir_status.f_frsize
        space_avaliable /= 1024 * 1024

        return (space_avaliable, "MB")

if __name__ == "__main__":
    path = "/"
    while True:
        time.sleep(10)
        num, unit = get_freespace(path)
        if num < LIMIT:
            print "freespace becoming low ..."
            print "try to shutdown system ..."
            os.chdir(os.getcwd())
            subprocess.Popen(["/home/johnson/apk/sys_control.py", "stop"])
            break

