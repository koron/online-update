#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# ZIPを解凍によるアップデート.

import logging
from zipfile import ZipFile

ZIP_PATH = 'tmp/vim73-kaoriya-win64-20110306.zip'
#ZIP_PATH = 'tmp/vim73-kaoriya-win64-20110412.zip'
OUTDIR = 'var'
CHECKSUM = 'var/check_sum.txt'

class Operation:
    TYPE_UPDATE = 1
    TYPE_DELETE = 2

    def __init__(self, type, path):
        self.type = type
        self.path = path

    def __str__(self):
        return "type=%d, path=%s" % (self.type, self.path)

class FileInfo:

    def __init__(self, name, size, hash):
        self.name = name
        self.size = size
        self.hash = hash

    @staticmethod
    def fromZipInfo(zipInfo):
        name = zipInfo.filename
        size = zipInfo.file_size
        crc32 = zipInfo.CRC
        fileInfo = FileInfo(name, size, crc32)
        return fileInfo

class ChecksumDatabase:
    OPTYPE_UPDATE = 1
    OPTYPE_DELETE = 2

    def __init__(self, path):
        self.path = path
        self.scannedFiles = []
        self.registeredFiles = []
        self.__loadCheck()

    def scanDir(self, dir):
        # TODO: ChecksumDatabase.scanDir
        pass

    def registerFile(self, fileInfo):
        self.registeredFiles.append(fileInfo)
        pass

    def operations(self):
        # TODO: consider scannedFiles.
        for i in self.registeredFiles:
            yield Operation(Operation.TYPE_UPDATE, i.name)

    def close(self):
        self.__saveCheck()

    def __loadCheck(self):
        # TODO: __loadCheck
        pass

    def __saveCheck(self):
        # TODO: __saveCheck
        pass

class FileStorage:

    def __init__(self, baseDir, zipFile):
        self.baseDir = baseDir
        self.zipFile = zipFile

    def execute(self, op):
        if op.type == Operation.TYPE_UPDATE:
            self.__update(op.path)
        elif op.type == Operation.TYPE_DELETE:
            self.__delete(op.path)
        else:
            logging.warning('Unknown optype: %d', op.type)

    def __update(self, op):
        print("update: %s" % op)
        # TODO: FileStorage.__update
        pass

    def __delete(self, op):
        print("delete: %s", op)
        # TODO: FileStorage.__delete
        pass

def isFile(zipInfo):
    # TODO: isFile
    return True

def unpackZip(zipPath, outDir, checkPath):
    # Open database and check existing files.
    checkDb = ChecksumDatabase(checkPath)
    checkDb.scanDir(outDir)

    # Register new files.
    zfile = ZipFile(zipPath, 'r')
    for zinfo in zfile.infolist():
        if isFile(zinfo):
            checkDb.registerFile(FileInfo.fromZipInfo(zinfo))

    # Update file storage.
    filestore = FileStorage(outDir, zfile)
    for op in checkDb.operations():
        filestore.execute(op)

    # End.
    zfile.close()
    checkDb.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unpackZip(ZIP_PATH, OUTDIR, CHECKSUM)
