#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Vimのアップデートを確認するプログラム.

from updater import OnlineUpdater
import logging
import os
import pe32
import sys

def __detectArch(rootdir):
    arch = pe32.ARCH_UNKNOWN
    exe = os.path.join(rootdir, 'vim.exe')
    if os.path.exists(exe):
        arch = pe32.detectArch(exe)
    else:
        machtype = os.environ.get('PROCESSOR_ARCHITECTURE').upper()
        if machtype == 'X86':
            arch = pe32.ARCH_WIN32
        elif machtype == 'AMD64':
            arch = pe32.ARCH_WIN64
    if arch != pe32.ARCH_WIN32 and arch != pe32.ARCH_WIN64:
        logging.error('failed to detect CPU arch')
    return arch

def __determineUrl(arch):
    if arch == pe32.ARCH_WIN32:
        logging.info('detected WIN32 version')
        return 'http://files.kaoriya.net/vim/vim73-kaoriya-win32.zip'
    elif arch == pe32.ARCH_WIN64:
        logging.info('detected WIN64 version')
        return 'http://files.kaoriya.net/vim/vim73-kaoriya-win64.zip'
    else:
        return None

def __update(rootdir):
    rootdir = rootdir.strip('"\'')
    url = __determineUrl(__detectArch(rootdir))
    if url:
        workdir = os.path.join(rootdir, 'online-update', 'var')
        recipe = os.path.join(workdir, 'recipe.txt')
        download = os.path.join(workdir, 'vim73.zip')
        updater = OnlineUpdater(url, rootdir, recipe, download)
        return updater.update()
    else:
        return 2

if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        # TODO:
        pass
    else:
        retval = __update(sys.argv[1])
        exit(retval)
