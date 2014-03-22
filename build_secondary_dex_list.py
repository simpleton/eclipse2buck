#!/usr/bin/python

import sys
import os
from eclipse2buck import decorator

def check_force_flag(lines):
    for line in lines:
        
        tag = "plugin.build.force="
        if line.startswith(tag):
            line = line.strip('\r\n')
            if (line[len(tag):] == "true"):
                return True
    return False
    
def extract_include(lines):
    if check_force_flag(lines):
        for line in lines:
            tag = "plugin.build.include="
            if line.startswith(tag):
                line = line.strip('\r\n')
                for item in line[len(tag):].split(" "):
                    if len(item) > 0:
                        print "\'" + item + "',"


@decorator.var("SECONDARY_DEX_PATTERN_LIST")
def print_secondary_pattern(folder):
    for dirname in os.listdir(folder):
        if os.path.isdir(folder+dirname) and (not dirname.startswith('.')):
            filename = folder+dirname + "/plugin.properties" 

            if os.path.isfile(filename):
                with open(filename) as fd:
                    extract_include(fd.readlines())


def dump_secondary_pattern(folder, outfile='./SECONDARY_DEX_PATTERN_LIST'):
    with open(outfile, 'w') as out:
        terminal = sys.stdout
        sys.stdout = out
        print_secondary_pattern(folder)
        sys.stdout = terminal

if __name__ == "__main__":
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = "./"
    print_secondary_pattern(root)
