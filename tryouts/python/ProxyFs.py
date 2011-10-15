#!/usr/bin/env python

#    Copyright (C) 2001  Jeff Epler  <jepler@unpythonic.dhs.org>
#    Copyright (C) 2006  Csaba Henk  <csaba.henk@creo.hu>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import os, sys
from errno import *
from stat import *
import fcntl
import logging
import hashlib

import fuse
from fuse import Fuse

LOG_FILENAME = "LOG"
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,)

if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)

def md5_file(fileName, block_size = 2 ** 20):
    md5 = hashlib.md5()
    try:
        fd = open(fileName,"rb")
    except IOError:
        return
    while True:
        data = fd.read(block_size)
        if not data:
            break
        md5.update(data)
    fd.close()
    return md5.hexdigest()

class Xmp(Fuse):

    def __init__(self, *args, **kw):

        Fuse.__init__(self, *args, **kw)

        self.root = "/home/cor/test"

        self.path_from_hash = {}
        self.hash_from_path = {}
        self.hasChanged = {}

    def getattr(self, path):
        return os.lstat("." + path)

    def readlink(self, path):
        return os.readlink("." + path)

    def readdir(self, path, offset):
        for e in os.listdir("." + path):
            yield fuse.Direntry(e)

    def unlink(self, path):
        path = "." + path
        os.unlink(path)
        self.path_from_hash.removes(path)

    def rmdir(self, path):
        os.rmdir("." + path)

    def symlink(self, path, path1):
        os.symlink(path, "." + path1)

    def rename(self, path, path1):
        os.rename("." + path, "." + path1)

    def link(self, path, path1):
        os.link("." + path, "." + path1)

    def chmod(self, path, mode):
        os.chmod("." + path, mode)

    def chown(self, path, user, group):
        os.chown("." + path, user, group)

    def truncate(self, path, len):
        f = open("." + path, "a")
        f.truncate(len)
        f.close()

    def mknod(self, path, mode, dev):
        os.mknod("." + path, mode, dev)

    def mkdir(self, path, mode):
        os.mkdir("." + path, mode)

    def utime(self, path, times):
        os.utime("." + path, times)

    def access(self, path, mode):
        if not os.access("." + path, mode):
            return -EACCES

    def open(self, path, flags):
        return 0

    def read(self, path, len, offset):
        path = "." + path

        f = open(path, "r")
        f.read()
        f.seek(offset)
        len = f.read(len)
        f.close()
        return len

    def write(self, path, buf, off):
        path = "." + path
 
        f = open(path, "a")
        f.seek(off)
        f.write(buf)
        f.seek(0);
        f.close();
 
        self.hasChanged[path] = True;
        return len(buf)

    def release(self, path, dh):
        path = "." + path

        digest = md5_file(path)

        # si le fichier existe
        if path in self.hash_from_path:
            if self.hasChanged[path] == True:
                self.hasChanged[path] = False
                #mise a jour
        else:

            if digest in self.path_from_hash:

                if path != self.path_from_hash[digest]:

                    os.remove(path)
                    os.link(self.path_from_hash[digest], path)
                    self.hash_from_path[path] = digest
                    logging.info("hard link %s %s" % (path, digest))

            else:
            
                self.path_from_hash[digest] = path
                self.hash_from_path[path] = digest
                logging.info("creation %s %s" % (path, digest))
            


    def releasedir(self, path, dh):
        logging.info("releasedir %s" % path)

    def fsinit(self):
        os.chdir(self.root)


def main():

    usage = """
Userspace nullfs-alike: mirror the filesystem tree from some point on.

""" + Fuse.fusage

    server = Xmp(version="%prog " + fuse.__version__,
                 usage=usage)

    server.parser.add_option(mountopt="root", metavar="PATH", default='/home/cor/test',
                             help="mirror filesystem from under PATH [default: %default]")
    server.parse(values=server, errex=1)

    try:
        if server.fuse_args.mount_expected():
            os.chdir(server.root)
    except OSError:
        print >> sys.stderr, "can't enter root of underlying filesystem"
        sys.exit(1)

    server.main()


if __name__ == '__main__':
    main()
