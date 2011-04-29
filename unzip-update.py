#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# ZIPを解凍によるアップデート.

import logging
from zipfile import ZipFile
from extractor import Extractor, ExtractionOptimizer, FileInfo

ZIP_PATH = 'tmp/vim73-kaoriya-win64-20110306.zip'
#ZIP_PATH = 'tmp/vim73-kaoriya-win64-20110412.zip'
OUTDIR = 'var/vim73-kaoriya-win64'
CHECKSUM = 'var/check_sum.txt'

def isFile(zipInfo):
    return zipInfo.filename[-1:] != '/'

def unpackZip(zipPath, outDir, checkPath):
    # Open database and check existing files.
    optimizer = ExtractionOptimizer(checkPath)
    optimizer.scanDir(outDir)

    # Register new files.
    zipFile = ZipFile(zipPath, 'r')
    for zipInfo in zipFile.infolist():
        if isFile(zipInfo):
            fileInfo = FileInfo.fromZipInfo(zipInfo, 1)
            optimizer.registerFile(fileInfo)

    # Update file storage.
    extractor = Extractor(outDir, zipFile)
    for op in optimizer.operations():
        extractor.extract(op)

    # End.
    zipFile.close()
    optimizer.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unpackZip(ZIP_PATH, OUTDIR, CHECKSUM)
