# -*- coding: utf-8 -*-

import logging
import os
from downloader import Downloader
from extractor import Extractor

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
    updater = OnlineUpdater( \
            'http://files.kaoriya.net/vim/vim73-kaoriya-win64.zip', \
            'var/vim73-kaoriya-win64', \
            'var/recipe.txt', \
            'var/vim73.zip')
    updater.update()
