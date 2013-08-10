#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Vimのアップデートを確認するプログラム.

import logging
import os
import sys
import gettext

from online_updater import Updater
from online_updater.progress import UpdaterProgress
import online_updater.pe32

pe32 = online_updater.pe32
_ = gettext.gettext

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
        return 'http://files.kaoriya.net/vim/vim74-kaoriya-win32.zip'
    elif arch == pe32.ARCH_WIN64:
        logging.info('detected WIN64 version')
        return 'http://files.kaoriya.net/vim/vim74-kaoriya-win64.zip'
    else:
        return None

class Progress(UpdaterProgress):

    def begin_download(self):
        print(_('Found update.'))
        UpdaterProgress.begin_download(self)

def update(target_dir):
    # Determine parameters.
    rootdir = target_dir.strip('"\'')
    url = __determineUrl(__detectArch(rootdir))
    if not url:
        print(_('Config error'))
        return
    # Execute the update.
    workdir = os.path.join(rootdir, 'online_updater', 'var')
    updater = Updater(name='vim74', url=url, target_dir=rootdir,
            work_dir=workdir, progress=Progress())
    result = updater.update()
    # Show result message.
    if result == Updater.COMPLETE:
        print(_('Updated successfully.'))
    elif result == Updater.INCOMPLETE:
        print(_('Incomplete update, retry later.'))
    elif result == Updater.STAY:
        print(_('No updates found.'))

if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        # TODO: show usage.
        pass
    else:
        retval = update(sys.argv[1])
        exit(retval)
