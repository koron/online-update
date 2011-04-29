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
from downloader import Downloader

URLROOT = 'http://files.kaoriya.net/vim/'
VIMZIP = 'vim73-kaoriya-win64.zip'
OUTDIR = 'var/vim73w64'

CHECK_URL = URLROOT + VIMZIP
LOCAL_FILE = VIMZIP

UPDATE_STATUS_STAY      = 0
UPDATE_STATUS_UPDATED   = 1
UPDATE_STATUS_ERROR     = 2

logging.basicConfig(level=logging.INFO)

"""
If-Modified-SinceをもつHTTPヘッダーを生成する.
"""
def getHeaderForChecking(path):
    if not os.path.exists(path):
        return {}
    else:
        mtime = os.path.getmtime(path)
        dt = datetime.fromtimestamp(mtime - 9 * 3600)
        since = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return { 'Accept': '*/*', 'If-Modified-Since': since }

def checkUpdateStatus(url, path):
    parsedUrl = urlparse(url)
    conn = httplib.HTTPConnection(parsedUrl[1])
    header = getHeaderForChecking(path)

    conn.request('GET', parsedUrl[2], None, header)

    status = UPDATE_STATUS_ERROR
    response = conn.getresponse()
    if response != None:
        if response.status == 304:
            logging.info('not updated')
            status = UPDATE_STATUS_STAY
        elif response.status == 200:
            logging.info('has updated')
            status = UPDATE_STATUS_UPDATED
        else:
            logging.warning('server failure: %d %s', \
                    response.status, response.reason)
    else:
        logging.critical('access failure')
    return (status, conn, response)

def downloadAs(resp, path):
    f = file(path, 'wb')
    try:
        f.write(resp.read())
    finally:
        f.close()

def unpackZip(zippath, outdir):
    # TODO: unzip-update.pyのunpackZipを呼び出す.
    pass

def check_vim_update(url, path, outdir):
    (status, conn, resp) = checkUpdateStatus(url, path)
    try:
        if status == UPDATE_STATUS_UPDATED:
            downloadAs(resp, path)
            unpackZip(path, outdir)
    finally:
        conn.close()

def getModifiedTime(path):
    if os.path.exists(path):
        return os.path.getmtime(path)
    else:
        return 0

def func():
    downloader = Downloader(CHECK_URL, LOCAL_FILE, \
            getModifiedTime(LOCAL_FILE))
    try:
        retval = downloader.download()
    finally:
        downloader.close()
    print('retval=%d' % retval)

if __name__ == '__main__':
    func()
    #check_vim_update(CHECK_URL, LOCAL_FILE, OUTDIR)
