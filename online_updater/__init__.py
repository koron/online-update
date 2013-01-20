# -*- coding: utf-8 -*-

import logging
import os
import sys
from online_updater.anchor import Anchor
from online_updater.downloader import Downloader, Downloader2
from online_updater.extractor import Extractor

class Updater:

    def __init__(self):
        self.downloader = None
        self.extractor = None

    def update(self):
        # TODO: setup these configuration variables.
        remote_url = None
        download_cache = None
        target_dir = None
        extract_cache = None
        anchor_path=None

        # Download update archive.
        anchor = Anchor(path=anchor_path)
        downloader = Downloader2(remote_url=remote_url,
                local_cache=download_cache, pivot_time=anchor.time)
        if downloader.download():
            anchor.update()
        elif downloader.has():
            # no newer update on remote, but has on local.
            pass
        else:
            # TODO: show message to user: "no updates"
            return False

        # Extract local update archive.
        extractor = Extractor2(download_cache, target_dir, extract_cache)
        if extractor.extract():
            downloader.clear()
        else:
            # TODO: show message to user:  "failed at extract, retry later"
            return False
        return True

    def restore(self):
        # TODO:
        return False

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
