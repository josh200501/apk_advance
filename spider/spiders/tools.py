#coding:utf-8
import hashlib
import logging
import time

def set_logger(program,log_file):
    logger = logging.getLogger(program)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.WARN)
    ch = logging.FileHandler(log_file)
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

def get_current_time():
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    str_time = time.strftime(ISOTIMEFORMAT,time.localtime(time.time()))
    return str_time

def utf8_to_gb2312(s):
    res = []
    for e in s:
      res.append(e.decode('utf-8').encode('gb2312'))
    return res

def sha1(s):
    return hashlib.sha1(s).hexdigest()

