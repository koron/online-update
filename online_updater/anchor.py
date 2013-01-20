# -*- coding: utf-8 -*-

import os

class Anchor:

    def __init__(self, path=None):
        self.path = path

    def update():
        # Dig a directory if not exists.
        (dir, name) = os.path.split(self.path)
        if len(dir) > 0 and not os.path.exists(dir):
            os.makedirs(dir)
        # Update last modified time of the anchor file.
        open(self.path, 'wb').close()

    @property
    def time(self):
        if os.path.exists(self.path):
            return os.path.getmtime(self.path)
        else:
            return 0
