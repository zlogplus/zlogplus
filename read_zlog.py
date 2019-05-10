# -*- coding: utf-8 -*-

import codecs

def read_zlog(filename):
    filename = str(filename)
    zlogfile = open(filename, 'r+b')
    while True:
        chunk = zlogfile.read(256)
        if not chunk:
            break
        print(chunk.hex())


if __name__ == "__main__":
    filename = input("filename: ")
    print(read_zlog(filename))
