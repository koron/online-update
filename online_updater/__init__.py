# -*- coding: utf-8 -*-

import logging
import os
import sys
from online_updater.anchor import Anchor
from online_updater.downloader import Downloader
from online_updater.extractor import Extractor

class Updater:

    def __init__(self, name, url, target_dir, work_dir):
        self.name = name
        self.url = url
        self.target_dir = target_dir
        self.work_dir = work_dir

    def update(self):
        # setup these configuration variables.
        remote_url = self.url
        target_dir = self.target_dir
        download_cache = os.path.join(self.work_dir, self.name + '.zip')
        extract_cache = os.path.join(self.work_dir, self.name + '-recipe.txt')
        anchor_path = os.path.join(self.work_dir, self.name + '-anchor.txt')

        # Download update archive.
        anchor = Anchor(path=anchor_path)
        downloader = Downloader(remote_url=remote_url,
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
        extractor = Extractor(download_cache, target_dir, extract_cache)
        if extractor.extractAll():
            downloader.clear()
        else:
            # TODO: show message to user:  "failed at extract, retry later"
            return False
        return True

    def restore(self):
        # TODO:
        return False
