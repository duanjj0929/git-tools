#!/usr/bin/env python3

import git
import os
import os.path as osp

SECTION_OPTION_VALUE_DICT = {
    "color": {
        "ui": "auto"
    },
    "core": {
        "autocrlf": "false",
        "editor": "vim"
    },
    "log": {
        "date": "iso"
    },
    "push": {
        "default": "simple"
    },
    "credential": {
        "helper": "store"
    },
}

if os.name == 'nt':
    SECTION_OPTION_VALUE_DICT["core"]["autocrlf"] = "true"

file_path = osp.normpath(osp.expanduser("~/.gitconfig"))

config_parser = git.config.GitConfigParser(file_path, read_only=False)

for section, option_value_dict in SECTION_OPTION_VALUE_DICT.items():
    for option, value in option_value_dict.items():
        config_parser.set_value(section, option, value)

config_parser.release()
