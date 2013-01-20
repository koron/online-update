# -*- coding: utf-8 -*-

import logging
import os
import sys
from online_updater.downloader import Downloader
from online_updater.extractor import Extractor

class OnlineUpdater:

    def __init__(self, url, unpackDir, recipeFile, downloadFile):
        self.url = url
        self.unpackDir = unpackDir
        self.recipeFile = recipeFile
        self.downloadFile = downloadFile

    def update(self):
        result = self.__download()
        if result == Downloader.RESULT_DOWNLOADED:
            self.__unpack()
            os.remove(self.downloadFile)
        return result

    def __download(self):
        downloader = Downloader(self.url, self.downloadFile, \
                OnlineUpdater.__getModifiedTime(self.recipeFile))
        try:
            retval = downloader.download()
        finally:
            downloader.close()
        return retval

    def __unpack(self):
        extractor = Extractor(self.downloadFile, self.unpackDir,
                self.recipeFile)
        extractor.extractAll()

    @staticmethod
    def __getModifiedTime(path):
        if os.path.exists(path):
            return os.path.getmtime(path)
        else:
            return 0

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        url = 'http://files.kaoriya.net/vim/vim73-kaoriya-win64.zip'
    else:
        url = 'http://files.kaoriya.net/vim/vim73-kaoriya-win64-%s.zip' \
                % sys.argv[1]
    updater = OnlineUpdater(url, 'var/vim73', \
            'var/recipe.txt', 'var/vim73.zip')
    updater.update()
