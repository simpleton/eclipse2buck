#!/usr/bin/python

import os
import fnmatch
from eclipse2buck import decorator

def find_all_files_with_suffix(relative_path, suffix):
    matches = []
    for root, dirnames, filenames in os.walk(relative_path):
        for filename in fnmatch.filter(filenames, suffix):
            matches.append(os.path.relpath(os.path.join(root,filename), relative_path))
    return matches


@decorator.var_with_comma("deps")
def gen_deps(deps):
    for dep in deps:
        print "'%s'," % dep

@decorator.var_with_comma("exported_deps")
def gen_exported_deps(exported_deps):
    for dep in exported_deps:
        print "'%s'," % dep


def path_get_parent(path):
    return os.path.abspath(os.path.join(path, os.pardir))

def path_get_basename(path):
    return os.path.splitext(os.path.basename(path))[0]
