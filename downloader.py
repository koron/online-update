# -*- coding: utf-8 -*-

from datetime import datetime
from urlparse import urlparse
import httplib
import logging
import os
import sys

logger = logging.getLogger('downloader')

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
            logger.warning('server failure: no response')
            return Downloader.RESULT_ERROR
        elif response.status == 304:
            logger.info('no updates.')
            return Downloader.RESULT_NOTMODIFIED
        elif response.status == 200:
            logger.info('downloading now.')

            # FIXME: unite into a function.
            (dir, name) = os.path.split(self.outPath)
            if len(dir) > 0 and not os.path.exists(dir):
                os.makedirs(dir)

            f = open(self.outPath, 'wb')
            try:
                f.write(response.read())
                return Downloader.RESULT_DOWNLOADED
            finally:
                f.close()
            logger.info('download completed.')
        else:
            logger.warning('server failure: %d %s', \
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
                logger.warning('server failure: no connection')
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 3:
        exit()

    modtime = 0
    if len(sys.argv) > 3 and os.path.exists(sys.argv[3]):
        modtime = os.path.getmtime(sys.argv[3])
    d = Downloader(sys.argv[1], sys.argv[2], modtime)
    d.download()
