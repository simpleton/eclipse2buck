import sys
import os

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

def find_all_plugin_properties(folder):
    for dirname in os.listdir(folder):
        if os.path.isdir(folder+dirname) and (not dirname.startswith('.')):
            filename = folder+dirname + "/plugin.properties" 

            if os.path.isfile(filename):
                with open(filename) as fd:
                    extract_include(fd.readlines())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = "./"
    print "SECONDARY_DEX_PATTERN_LIST = ["
    find_all_plugin_properties(root)
    print "]"
