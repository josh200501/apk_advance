#!/usr/bin/env python
#encoding:utf8

import os

def get_env_para():
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    store_dir = "store"
    log_dir = "log"
    cfg_name = "config.ini"

    store_path = os.path.join(parent_dir, store_dir)
    log_path = os.path.join(parent_dir, log_dir)
    cfg_path = os.path.join(parent_dir, cfg_name)

    if not os.path.isfile(cfg_path):
        print "no config.ini, will exit."
        sys.exit(1)

    #print (cfg_path, store_path, log_path)
    return (cfg_path, store_path, log_path)

if __name__ == "__main__":
    get_env_para()
