#!/usr/bin/python

import sys
import os
from eclipse2buck import decorator
from eclipse2buck import config

def get_current_dep_name(file):
    if os.path.isdir(file):
        return os.path.realpath(file)
    else:
        return os.path.dirname(os.path.realpath(file))

def get_reference_lists(file):
    filename = get_current_dep_name(file) + '/project.properties';
    deps = []
    with open(filename) as fd:
        lines = fd.readlines()
        for line in lines:
            if line.startswith("android.library.reference."):
                deps.append(line.split("/")[-1].strip("\r\n"))
    
    return deps

@decorator.var("DEPS")
def print_binary_deps(root):
    deps = get_reference_lists(root)
    for dep in deps:
            print "'//%s:%s%s'," % (dep, dep, config.proj_suffix)

def dump_binary_deps(root, outfile="./DEPS"):
    with open(outfile, 'w') as out:
        terminal = sys.stdout
        sys.stdout = out
        print_binary_deps(root)
        sys.stdout = terminal

def check_is_lib(file):
    filename = get_current_dep_name(file) + '/project.properties';
    with open(filename) as fd:
        lines = fd.readlines()
        for line in lines:
            tag = "android.library="
            if line.startswith(tag):
                if (line[len(tag):].strip("\r\n") == "true"):
                    return True
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = os.getcwd()

    print_binary_deps(root)
