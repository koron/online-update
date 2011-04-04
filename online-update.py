#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Vimのアップデートを確認するプログラム.

from datetime import datetime
from urlparse import urlparse
import httplib
import logging
import os
import time

URLROOT = 'http://files.kaoriya.net/vim/'
VIMZIP = 'vim73-kaoriya-win64.zip'
OUTDIR = 'var/vim73w64'

CHECK_URL = URLROOT + VIMZIP
LOCAL_FILE = VIMZIP

UPSTATUS_STAY       = 0
UPSTATUS_UPDATED    = 1
UPSTATUS_ERROR      = 2

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

def unpack_zip(zippath, outdir):
    # TODO:
    pass

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
    check_vim_update(CHECK_URL, LOCAL_FILE, OUTDIR)