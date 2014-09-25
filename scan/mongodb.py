# encoding:utf8

import pymongo
import ConfigParser
import os

CFG = "../config.ini"

cf_path = os.path.join(os.getcwd(), CFG)
cf = ConfigParser.ConfigParser()
cf.read(cf_path)

DB_ADDR = cf.get("database", "addr")
DB_PORT = int(cf.get("database", "port"), 10)

READONLY = cf.get("database", "readonly_user")
READONLY_PASSWD = cf.get("database", "readonly_password")

READWRITE = cf.get("database", "readwrite_user")
READWRITE_PASSWD = cf.get("database", "readwrite_password")

def connect_readwrite():
    db = None
    try:
        con = pymongo.Connection(DB_ADDR, DB_PORT)
        db = con.mydb
        db.authenticate(READWRITE, READWRITE_PASSWD)
    except:
        print "Database connect error."
    return db

def connect_readonly():
    db = None
    try:
        con = pymongo.Connection(DB_ADDR, DB_PORT)
        db = con.mydb
        db.authenticate(READONLY, READONLY_PASSWD)
    except:
        print "Database connect error."
    return db


