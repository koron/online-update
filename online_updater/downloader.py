# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import os
import sys

if sys.version_info >= (3, 0, 0):
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
else:
    from urllib2 import HTTPError, Request, urlopen

logger = logging.getLogger('downloader')

def header(pivot_time):
    if pivot_time == 0:
        return {}
    else:
        # FIXME: "9 * 3600" must be got from timezone.
        dt = datetime.fromtimestamp(pivot_time - 9 * 3600)
        since = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return { 'If-Modified-Since': since }

def save_as(response, path):
    # Dig a directory if not exists.
    (dir, name) = os.path.split(path)
    if len(dir) > 0 and not os.path.exists(dir):
        os.makedirs(dir)
    # Write response body to a file.
    f = open(path, 'wb')
    try:
        f.write(response.read())
    finally:
        f.close()

class Downloader2:

    def __init__(self, remote_url=None, local_cache=None, pivot_time=0):
        if not remote_url:
            raise Exception('\'remote_url\' is not provided.')
        if not local_cache:
            raise Exception('\'local_cache\' is not provided.')
        self.remote_url = remote_url
        self.local_cache = local_cache
        self.pivot_time = pivot_time

    def has(self):
        return os.path.exists(self.local_cache)

    def download(self):
        # Emit a HTTP request.
        try:
            response = urlopen(Request(self.remote_url, header(pivot_time)))
        except HTTPError as e:
            response = e
        # Parse a HTTP response.
        try:
            if response.code == 304:
                return False
            elif response.code == 200:
                tmp = self.local_cache + '.download'
                save_as(response, tmp)
                self.clear()
                os.rename(tmp, self.local_cache)
            else:
                raise Exception('unexpected response: %d' % response.code)
        finally:
            if response:
                response.close()
        return True

    def clear(self):
        if self.has():
            os.remove(self.local_cache)

class Downloader:

    RESULT_NOTMODIFIED  = 0
    RESULT_DOWNLOADED   = 1
    RESULT_ERROR        = 2

    def __init__(self, inUrl, outPath, modifiedTime=0):
        self.inUrl = inUrl
        self.outPath = outPath
        self.modifiedTime = modifiedTime

    def download(self):
        response = self.__getReponse()
        try:
            return self.__download(response)
        finally:
            if response:
                response.close()

    def __download(self, response):
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
        retval = None
        header = self.__getHeader()
        request = Request(self.inUrl, None, header)
        try:
            retval = urlopen(request)
        except HTTPError as e:
            retval = e
        except:
            logger.warning('server failure: no connection')
        return retval

    def close(self):
        pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 3:
        exit()

    modtime = 0
    if len(sys.argv) > 3 and os.path.exists(sys.argv[3]):
        modtime = os.path.getmtime(sys.argv[3])
    d = Downloader(sys.argv[1], sys.argv[2], modtime)
    d.download()
