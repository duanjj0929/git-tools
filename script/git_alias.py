#!/usr/bin/env python3

import git
import os.path as osp

ALIAS_SECTION = "alias"

OPTION_VALUE_DICT = {
    "br": "branch",
    "ci": "commit",
    "co": "checkout",
    "df": "diff",
    "last": "log -1 HEAD",
    "st": "status",
    "unstage": "reset HEAD --",
}

file_path = osp.normpath(osp.expanduser("~/.gitconfig"))

config_parser = git.config.GitConfigParser(file_path, read_only=False)

for option, value in OPTION_VALUE_DICT.items():
    config_parser.set_value(ALIAS_SECTION, option, value)

config_parser.release()
