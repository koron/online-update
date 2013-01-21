# -*- coding: utf-8 -*-

import logging
import os
import sys
from online_updater.anchor import Anchor
from online_updater.downloader import Downloader
from online_updater.extractor import Extractor

class Updater:

    COMPLETE, INCOMPLETE, STAY = range(3)

    def __init__(self, name=None, url=None, target_dir=None, work_dir=None,
            progress=None):
        if not name:
            raise Exception('\'name\' is not provided.')
        if not url:
            raise Exception('\'url\' is not provided.')
        if not target_dir:
            raise Exception('\'target_dir\' is not provided.')
        if not work_dir:
            raise Exception('\'work_dir\' is not provided.')
        self.name = name
        self.url = url
        self.target_dir = target_dir
        self.work_dir = work_dir
        self.progress = progress

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
                local_cache=download_cache, pivot_time=anchor.time,
                progress=self.progress)
        if downloader.download():
            anchor.update()
        elif downloader.has():
            # no newer update on remote, but has on local.
            pass
        else:
            # no update on both remote and local.
            return Updater.STAY

        # Extract local update archive.
        extractor = Extractor(download_cache, target_dir, extract_cache,
                self.progress)
        if extractor.extractAll():
            downloader.clear()
        else:
            # incomplete, retry later
            # failed at extract, retry later.
            return Updater.INCOMPLETE
        return Updater.COMPLETE

    def restore(self):
        # FIXME: implement in future.
        return False
