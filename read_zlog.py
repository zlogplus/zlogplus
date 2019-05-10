# -*- coding: utf-8 -*-

def read_zlog(filename):
	filename = str(filename)
  zlogfile = open(filename, 'r+b')



if __name__ == "__main__":
	filename = input("filename: ")
	print(read_zlog(filename))
