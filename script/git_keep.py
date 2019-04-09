#!/usr/bin/env python3

import getopt
import os
import sys

# 起始目录
STARTING_POINT = None
# 文件名称
KEEP_FILE = ".gitkeep"

try:
    shortopts = "hd:f:"
    longopts = ["help", "directory=", "file="]
    opts, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
except getopt.GetoptError:
    print("usage: {} -d <starting-point> [-f <keep-file>]".format(sys.argv[0]))
    sys.exit(1)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print("usage: {} -d <starting-point> [-f <keep-file>]".format(
            sys.argv[0]))
        sys.exit()
    elif opt in ("-d", "--directory"):
        STARTING_POINT = arg
    elif opt in ("-f", "--file"):
        KEEP_FILE = arg
    else:
        print("usage: {} -d <starting-point> [-f <keep-file>]".format(
            sys.argv[0]))
        sys.exit(1)

if not STARTING_POINT:
    print("usage: {} -d <starting-point> [-f <keep-file>]".format(sys.argv[0]))
    sys.exit(1)

command = "find {} -type d -empty -exec touch {{}}/{} \\;".format(
    STARTING_POINT, KEEP_FILE)
os.system(command)
