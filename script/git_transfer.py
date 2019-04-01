#!/usr/bin/env python3

import git
import os
import shutil

# 获取源 git url
source_git_url = input("Source Git URL: ")

# 获取目标 git url
target_git_url = input("Target Git URL: ")

# 清理clone目录(如果需要)
print("Preparing")
(head, tail) = os.path.split(source_git_url)
clone_to_path = tail

if os.path.exists(clone_to_path):
    shutil.rmtree(clone_to_path)

# 从原地址克隆一份裸版本库
print("Clone from {}".format(source_git_url))
cloned_repo = git.Repo.clone_from(source_git_url, clone_to_path, bare=True)

# 以镜像推送的方式上传代码到target
print("Push to {}".format(target_git_url))
remote = cloned_repo.create_remote("target", target_git_url)
remote.push(mirror=True)

# 清理clone目录
print("Finishing")
shutil.rmtree(clone_to_path)

print("Done")
