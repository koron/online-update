#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Vimのアップデートを確認するプログラム.

import logging
from updater import OnlineUpdater

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    updater = OnlineUpdater( \
            'http://files.kaoriya.net/vim/vim73-kaoriya-win64.zip', \
            'var/vim73-kaoriya-win64', \
            'var/recipe.txt', \
            'var/vim73.zip')
    updater.update()
