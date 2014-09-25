# coding:utf8

import os
import sys
import mongodb
import tools
import time

SAMPLE_PATH = "/home/johnson/apk_sample"

file_info_tep = {
        "name": "",
        "md5": "",
        "url": "",
        "date": "",
        "type_tag": "none",
        "scan_status": "none",
        "archive_flag": "none"
        }

def get_file_info(sample_path):
    if os.path.exists(sample_path):
        file_list = walk_dir(sample_path)
    else:
        print "No sample folder."
        sys.exit(1)

    for i in file_list:
        fp = os.path.join(SAMPLE_PATH, i)
        md5 = tools.md5sum(fp)
        if check_dup(md5):
            file_info_tep["dup"] = True
            file_info_tep["scan_status"] = "dup"
        file_info_tep["name"] = fp
        file_info_tep["md5"] = md5
        file_info_tep["date"] = time.strftime(
                "%Y%m%d-%H:%M:%S",
                time.localtime())
        ins_file_info(file_info_tep)

def ins_file_info(file_info):
    db = mongodb.connect_readwrite()
    collection = db.file_info_list
    collection.insert(file_info)

def check_dup(md5):
    db = mongodb.connect_readwrite()
    collection = db.file_info_list
    collection.update({"md5":md5}, {"$set":{"md5":md5}})
    res = db.command({"getLastError": 1})
    if res["updatedExisting"]:
        return True
    else:
        return False

def walk_dir(rootDir):
    length = len(rootDir)
    file_list_cont = []
    list_dir = os.walk(rootDir)
    for root, dirs, files in list_dir:
        for f in files:
            file_list_cont.append(os.path.join(root, f)[length+1:])

    return file_list_cont


def main():
    get_file_info(SAMPLE_PATH)

if __name__ == "__main__":
    main()

