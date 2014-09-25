#-*- coding:utf8 -*-

import logging
import hashlib
import sys

def set_logger(prog_name, log_path):
    # create a logger
    logger = logging.getLogger(prog_name)
    logger.setLevel(logging.DEBUG)

    # create a handler inorder to write log into file
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)

    # create another handler to send info to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # define handler's ouput format
    formatter = logging.Formatter(
            '%(asctime)s - \
            %(module)s.%(funcName)s.%(lineno)d - \
            %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    # log one
    # logger.info('hello')
    return logger

"""
compute file or strings hashvalue.
"""
def sumfile_md5(fobj):
    m = hashlib.md5()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

def md5sum(fname):
    ret = ""
    if fname == '-':
        ret = sumfile_md5(sys.stdin)
    else:
        try:
            f = file(fname, 'rb')
        except:
            print 'Failed to open file: ', fname
            return False
        try:
            ret = sumfile_md5(f)
            f.close()
        except:
            pass

    return ret

def sumfile_sha1(fobj):
    m = hashlib.sha1()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

def sha1sum(fname):
    if fname == '-':
        ret = sumfile_sha1(sys.stdin)
    else:
        try:
            f = file(fname, 'rb')
        except:
            return 'Failed to open file'
        ret = sumfile_sha1(f)
        f.close()
    return ret

def sumfile_sha256(fobj):
    m = hashlib.sha256()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

def sha256sum(fname):
    if fname == '-':
        ret = sumfile_sha256(sys.stdin)
    else:
        try:
            f = file(fname, 'rb')
        except:
            return 'Failed to open file'
        ret = sumfile_sha256(f)
        f.close()
    return ret

if __name__ == '__main__':
    pass
