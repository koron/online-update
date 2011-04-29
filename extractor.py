# -*- coding: utf-8 -*-

import binascii
import logging
import os

class FileInfo:

    def __init__(self, name, size, hash):
        self.name = name.replace('\\', '/')
        self.size = size
        self.hash = hash
        self.origName = name

    def __str__(self):
        return 'FileInfo<name=%s,size=%d,hash=%08x>' % \
                (self.name, self.size, self.hash)

    def __eq__(self, other):
        return other != None and self.size == other.size and \
                self.hash == other.hash and self.name == other.name

    @staticmethod
    def fromZipInfo(zipInfo, strip=0):
        name = zipInfo.filename
        if strip > 0:
            elements = name.split('/')
            name = '/'.join(elements[strip:])
        size = zipInfo.file_size
        crc32 = zipInfo.CRC
        fileInfo = FileInfo(name, size, crc32)
        fileInfo.zipFilename = zipInfo.filename
        return fileInfo

class ExtractOperation:
    TYPE_UNMANAGE = 0
    TYPE_SKIP     = 1
    TYPE_UPDATE   = 2
    TYPE_DELETE   = 3
    TYPE_KEEP     = 4

    def __init__(self, type, fileInfo):
        self.type = type
        self.fileInfo = fileInfo

    def __str__(self):
        return 'ExtractOperation<type=%d,fileInfo=%s>' % \
                (self.type, self.fileInfo)

class ExtractionOptimizer:

    def __init__(self, path):
        self.path = path
        self.knownFiles = []
        self.scannedFiles = []
        self.registeredFiles = []
        self.__loadCheck()

    def scanDir(self, dir):
        try:
            self.__scanDir(dir, None)
        except:
            pass

    def registerFile(self, fileInfo):
        self.registeredFiles.append(fileInfo)
        pass

    def operations(self):
        knownTable = ExtractionOptimizer.__toTable(self.knownFiles)
        scannedTable = ExtractionOptimizer.__toTable(self.scannedFiles)

        # Check updated files.
        for i in self.registeredFiles:
            if i.name in knownTable:
                del knownTable[i.name]
            scanned = scannedTable.get(i.name)
            if scanned:
                del scannedTable[i.name]
            if i == scanned:
                yield ExtractOperation(ExtractOperation.TYPE_SKIP, i)
            else:
                yield ExtractOperation(ExtractOperation.TYPE_UPDATE, i)

        # Check deleted files.
        for i in self.knownFiles:
            if not knownTable.has_key(i.name):
                continue
            scanned = scannedTable.get(i.name)
            if scanned:
                del scannedTable[i.name]
            if i == scanned:
                yield ExtractOperation(ExtractOperation.TYPE_DELETE, i)
            else:
                yield ExtractOperation(ExtractOperation.TYPE_KEEP, i)

        for i in scannedTable.values():
            yield ExtractOperation(ExtractOperation.TYPE_UNMANAGE, i)

    def close(self):
        self.__saveCheck()

    def __scanDir(self, root, subdir):
        dir = os.path.join(root, subdir) if subdir else root
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            key  = os.path.join(subdir, name) if subdir else name
            if os.path.isdir(path):
                self.__scanDir(root, key)
            elif os.path.isfile(path):
                fileInfo = ExtractionOptimizer.__toFileInfo(path, key)
                if fileInfo:
                    self.scannedFiles.append(fileInfo)

    def __loadCheck(self):
        if not os.path.exists(self.path):
            return
        for line in open(self.path, 'r'):
            fileInfo = ExtractionOptimizer.__parse(line)
            if fileInfo:
                self.knownFiles.append(fileInfo)

    def __saveCheck(self):
        f = open(self.path, 'w')
        for fileInfo in self.registeredFiles:
            f.write(ExtractionOptimizer.__format(fileInfo))
        f.close()

    @staticmethod
    def __toTable(fileInfoArray):
        table = {}
        for i in fileInfoArray:
            table[i.name] = i
        return table

    @staticmethod
    def __toFileInfo(path, key):
        name = key
        size = os.path.getsize(path)
        hash = ExtractionOptimizer.__calcCrc32(path)
        if size >= 0 and hash != None:
            return FileInfo(name, size, hash)

    @staticmethod
    def __calcCrc32(path):
        f = open(path, 'rb')
        crc32 = binascii.crc32(f.read())
        if crc32 < 0:
            crc32 += 0x100000000
        f.close()
        return crc32

    @staticmethod
    def __parse(line):
        items = line[:-1].split('\t')
        return FileInfo(items[0], int(items[1]), int(items[2], 16))

    @staticmethod
    def __format(fileInfo):
        return '%s\t%d\t%08x\n' % \
                (fileInfo.name, fileInfo.size, fileInfo.hash)

class Extractor:

    def __init__(self, baseDir, zipFile):
        self.baseDir = baseDir
        self.zipFile = zipFile

    def extract(self, op):
        if op.type == ExtractOperation.TYPE_UNMANAGE:
            self.__unmanage(op)
        elif op.type == ExtractOperation.TYPE_SKIP:
            self.__skip(op)
        elif op.type == ExtractOperation.TYPE_UPDATE:
            self.__update(op)
        elif op.type == ExtractOperation.TYPE_DELETE:
            self.__delete(op)
        elif op.type == ExtractOperation.TYPE_KEEP:
            self.__keep(op)
        else:
            logging.warning('Unknown optype: %d', op.type)

    def __unmanage(self, op):
        # Currently, nothing to do.
        logging.debug('unmanage: %s', op.fileInfo.name)
        pass

    def __skip(self, op):
        # Currently, nothing to do.
        logging.debug('skip: %s', op.fileInfo.name)
        pass

    def __update(self, op):
        path = os.path.join(self.baseDir, op.fileInfo.origName)
        logging.debug('update: %s', path)
        (dir, name) = os.path.split(path)
        zipname = op.fileInfo.zipFilename

        if not os.path.exists(dir):
            os.makedirs(dir)
        of = open(path, 'wb')
        of.write(self.zipFile.read(zipname))
        of.close()

    def __delete(self, op):
        path = os.path.join(self.baseDir, op.fileInfo.origName)
        logging.debug('delete: %s', path)
        os.remove(path)
        pass

    def __keep(self, op):
        # Currently, nothing to do.
        logging.debug('keep: %s', op.fileInfo.name)
        pass

