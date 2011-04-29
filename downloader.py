# -*- coding: utf-8 -*-

from datetime import datetime
from urlparse import urlparse
import httplib

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
