# -*- coding: utf-8 -*-

import sys

class StdoutProgress:

    WIDTH = 50

    def __init__(self, name):
        self.name = name
        self.size = StdoutProgress.WIDTH
        self.current = 0

    def start(self):
        sys.stdout.write('%s  [%s]' % (self.name, ' ' * self.size))
        sys.stdout.flush()
        sys.stdout.write('\b' * (self.size + 1))

    def change(self, value, max):
        if max <= 0:
            return
        value = int(value * self.size / max)
        if value > self.current:
            sys.stdout.write('=' * (value - self.current))
            self.current = value

    def end(self):
        if self.current < self.size:
            sys.stdout.write('-' * (self.size - self.current))
        sys.stdout.write('\n')
        sys.stdout.flush()

class UpdaterProgress:

    def __init__(self):
        self.downloadProgress = StdoutProgress(' * 1/2  Download')
        self.extractProgress = StdoutProgress(' * 2/2  Extract ')

    def begin_download(self):
        self.downloadProgress.start()

    def do_download(self, value, max):
        self.downloadProgress.change(value, max)

    def end_download(self):
        self.downloadProgress.end()

    def begin_extract(self, *args):
        self.extractProgress.start()

    def do_extract(self, value, max):
        self.extractProgress.change(value, max)

    def end_extract(self, *args):
        self.extractProgress.end()
