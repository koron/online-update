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

UPDATE_STATUS_STAY      = 0
UPDATE_STATUS_UPDATED   = 1
UPDATE_STATUS_ERROR     = 2

logging.basicConfig(level=logging.INFO)

class Downloader:

    RESULT_NOTMODIFIED  = 0
    RESULT_DOWNLOADED   = 1
    RESULT_ERROR        = 2

    def __init__(self, inUrl, outPath, modifiedTime=0):
        self.inUrl = inUrl
        self.parsedUrl = urlparse(self.inUrl)
        self.outPath = outPath
        self.connection = None
        self.response = None
        self.modifiedTime = modifiedTime

    def download(self):
        response = self.__getReponse()
        if not response:
            logging.warning('server failure: no response')
            return Downloader.RESULT_ERROR
        elif response.status == 304:
            return Downloader.RESULT_NOTMODIFIED
        elif response.status == 200:
            f = open(self.outPath, 'wb')
            try:
                f.write(response.read())
                return Downloader.RESULT_DOWNLOADED
            finally:
                f.close()
        else:
            logging.warning('server failure: %d %s', \
                    response.status, response.reason)
            return Downloader.RESULT_ERROR

    def __getConnection(self):
        if not self.connection:
            self.connection = httplib.HTTPConnection(self.parsedUrl[1])
            #self.connection.set_debuglevel(1)
        return self.connection

    def __getHeader(self):
        if self.modifiedTime == 0:
            return {}
        else:
            # FIXME: 9 * 3600 must be got from timezone.
            dt = datetime.fromtimestamp(self.modifiedTime - 9 * 3600)
            since = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
            return { 'If-Modified-Since': since }

    def __getReponse(self):
        if not self.response:
            connection = self.__getConnection()
            if not connection:
                logging.warning('server failure: no connection')
                return None
            else:
                header = self.__getHeader()
                connection.request('GET', self.parsedUrl[2], None, header)
                self.response = connection.getresponse()
        return self.response

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

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
