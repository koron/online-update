#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Vimのアップデートを確認するプログラム.

from datetime import datetime
from urlparse import urlparse
import httplib
import logging
import os
import time
from zipfile import ZipFile

URLROOT = 'http://files.kaoriya.net/vim/'
VIMZIP = 'vim73-kaoriya-win64.zip'
OUTDIR = 'var/vim73w64'

CHECK_URL = URLROOT + VIMZIP
LOCAL_FILE = VIMZIP

UPSTATUS_STAY       = 0
UPSTATUS_UPDATED    = 1
UPSTATUS_ERROR      = 2

UNPACK_STATUS_KEEP      = 0
UNPACK_STATUS_EXTRACT   = 1
UNPACK_STATUS_UNKNOWN   = 2

logging.basicConfig(level=logging.INFO)

"""
If-Modified-SinceをもつHTTPヘッダーを生成する.
"""
def get_check_header(path):
    if not os.path.exists(path):
        return {}
    st = os.stat(path)
    if st == None:
        return {}
    else:
        dt = datetime.fromtimestamp(st.st_mtime - 9 * 3600)
        since = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return { 'Accept': '*/*', 'If-Modified-Since': since }

def check_upstatus(url, path):
    p = urlparse(url)
    c = httplib.HTTPConnection(p[1])
    h = get_check_header(path)
    #c.set_debuglevel(1)
    c.request('GET', p[2], None, get_check_header(path))
    s = UPSTATUS_ERROR
    r = c.getresponse()
    if r != None:
        if r.status == 304:
            logging.info('not updated')
            s = UPSTATUS_STAY
        elif r.status == 200:
            logging.info('has updated')
            s = UPSTATUS_UPDATED
        else:
            logging.warning('server failure: %d %s', r.status, r.reason)
    else:
        logging.critical('access failure')
    return (s, c, r)

def download_as(resp, path):
    f = file(path, 'wb')
    try:
        f.write(resp.read())
    finally:
        f.close()

def zipinfo2fileinfo(zipinfo, outdir):
    # TODO
    return None

def newinfo2oldinfo(newinfo):
    # TODO
    return None

def check_unpack_status(newinfo, oldinfo):
    # TODO
    return UNPACK_STATUS_KEEP

def unpack_entry(zipfile, newinfo):
    # TODO
    pass

def unpack_zip(zippath, outdir):
    zfile = ZipFile(zippath, 'r')
    for zinfo in zfile.infolist():
        newinfo = zipinfo2fileinfo(zinfo, outdir)
        oldinfo = newinfo2oldinfo(newinfo)
        status = check_unpack_status(newinfo, oldinfo)
        if status == UNPACK_STATUS_KEEP:
            pass
        elif status == UNPACK_STATUS_EXTRACT:
            unpack_entry(zfile, newinfo)
        elif status == UNPACK_STATUS_UNKNOWN:
            pass
        else:
            logging.critical('unknown unpack_status: %d', status)
    zfile.close()

def update_vim(resp, path, outdir):
    download_as(resp, path)
    unpack_zip(path, outdir)

def check_vim_update(url, path, outdir):
    (status, conn, resp) = check_upstatus(url, path)
    try:
        if status == UPSTATUS_UPDATED:
            update_vim(resp, path)
    finally:
        conn.close()

if __name__ == '__main__':
    #check_vim_update(CHECK_URL, LOCAL_FILE, OUTDIR)
    unpack_zip(LOCAL_FILE, OUTDIR)
