#!/usr/bin/env python3

import getopt
import git
import os
import shutil
import sys

# 命令行参数解析
from_git_url = None
to_git_url = None

try:
    opts, args = getopt.getopt(sys.argv[1:], "hf:t:", ["help", "from=", "to="])
except getopt.GetoptError:
    print("usage: {} -f <from_git_url> -t <to_git_url>".format(sys.argv[0]))
    sys.exit(1)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print("usage: {} -f <from_git_url> -t <to_git_url>".format(
            sys.argv[0]))
        sys.exit()
    elif opt in ("-f", "--from"):
        from_git_url = arg
    elif opt in ("-t", "--to"):
        to_git_url = arg
    else:
        print("usage: {} -f <from_git_url> -t <to_git_url>".format(
            sys.argv[0]))
        sys.exit(1)

if (not from_git_url) or (not to_git_url):
    print("usage: {} -f <from_git_url> -t <to_git_url>".format(sys.argv[0]))
    sys.exit(1)

# 清理clone目录(如果需要)
print("Preparing")
(head, tail) = os.path.split(from_git_url)
clone_to_path = tail

if os.path.exists(clone_to_path):
    shutil.rmtree(clone_to_path)

# 从原地址克隆一份裸版本库
print("Clone from {}".format(from_git_url))
cloned_repo = git.Repo.clone_from(from_git_url, clone_to_path, bare=True)

# 以镜像推送的方式上传代码到目标地址
print("Push to {}".format(to_git_url))
dest_remote = cloned_repo.create_remote("dest", to_git_url)
dest_remote.push(mirror=True)

# 清理clone目录
print("Finishing")
shutil.rmtree(clone_to_path)

print("Done")
