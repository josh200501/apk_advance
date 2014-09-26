#!/usr/bin/env python
#encoding:utf8

import subprocess
import os
import sys

PID_FILE = "/home/johnson/apk/log/pidfile"

def start():
    if os.path.isfile(PID_FILE):
        try:
            os.remove(PID_FILE)
        except:
            print "error on delete file: {0}".format(PID_FILE)
    to_exec = ["downloader.py", "scanner.py", "store.py"]
    exec_path = "/home/johnson/apk/apk_scan/"
    subprocess.Popen("/home/johnson/apk/monitor.py")
    os.chdir(exec_path)
    for i in to_exec:
        abs_exec_path = os.path.join(exec_path, i)
        subprocess.Popen(abs_exec_path)

def stop():
    fp = open(PID_FILE)
    pids = fp.readlines()
    fp.close()
    for i in pids:
        i = i.strip()
        if not i:
            continue
        subprocess.call(["kill", "-9", i])
        print "kill process: {0}".format(i)

def main(cmd):
    if cmd == "start":
        start()
    elif cmd == "stop":
        stop()
    else:
        print "invalid param: {0}".format(cmd)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: ./sys_control.py [start, stop]"
        sys.exit(1)
    cmd = sys.argv[1]
    main(cmd)
