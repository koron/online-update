# -*- coding: utf-8 -*-

from datetime import datetime
import urllib2
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
        self.outPath = outPath
        self.response = None
        self.modifiedTime = modifiedTime

    def download(self):
        response = self.__getReponse()
        if not response:
            logger.warning('server failure: no response')
            return Downloader.RESULT_ERROR
        elif response.code == 304:
            logger.info('no updates.')
            return Downloader.RESULT_NOTMODIFIED
        elif response.code == 200:
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
                    response.code, response.msg)
            return Downloader.RESULT_ERROR

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
            header = self.__getHeader()
            request = urllib2.Request(self.inUrl, None, header)
            try:
                self.response = urllib2.urlopen(request)
            except urllib2.HTTPError, e:
                self.response = e
            except:
                logger.warning('server failure: no connection')
                return None
        return self.response

    def close(self):
        if self.response:
            self.response.close()
            self.response = None

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 3:
        exit()

    modtime = 0
    if len(sys.argv) > 3 and os.path.exists(sys.argv[3]):
        modtime = os.path.getmtime(sys.argv[3])
    d = Downloader(sys.argv[1], sys.argv[2], modtime)
    d.download()
