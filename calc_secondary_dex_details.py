#!/usr/bin/python

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
    patterns = []
    if check_force_flag(lines):
        for line in lines:
            tag = "plugin.build.include="
            if line.startswith(tag):
                line = line.strip('\r\n')
                for item in line[len(tag):].split(" "):
                    if len(item) > 0:
                        patterns.append(item)
    return patterns

def find_all_plugin_properties(folder):
    maps = {}
    for dirname in os.listdir(folder):
        if os.path.isdir(folder+dirname) and (not dirname.startswith('.')):
            filename = folder+dirname + "/plugin.properties" 

            if os.path.isfile(filename):
                with open(filename) as fd:
		    patterns = extract_include(fd.readlines())
		    if len(patterns) > 0:
			for pattern in patterns:
			    maps[pattern] = dirname
    return maps
                    
def calc_size(file):
    secondary_size = 0
    methods_num = 0
    with open(file, "r") as fd:
        lines = fd.readlines()
        for line in lines:
            size, num, path = line.split(" ")
            secondary_size += int(size)
            methods_num += int(num)
    return secondary_size >> 10, methods_num

def calc_plugin_module_size(file, module_maps):
    modules_size = {}
    modules_methods = {}
    for value in module_maps.values():
	modules_size[value] = 0
        modules_methods[value] = 0
    with open(file, "r") as fd:
	lines = fd.readlines()
	for line in lines:
            size, methods_num, path = line.split(" ")
            for value in module_maps.keys():
                if (path.startswith(value)):
                    modules_size[module_maps[value]] += int(size)
                    modules_methods[module_maps[value]] += int(methods_num)
    for key, size in modules_size.iteritems():
       modules_size[key] = size >> 10

    return modules_size, modules_methods
	    

if __name__ == "__main__":
    """
    calc sub module's linearalloc size
    """
    TAG = "[LinearAlloc]"
    if len(sys.argv) > 2:
        root = sys.argv[1]
        target = sys.argv[2]
    else:
        root = "./"
        target = "release"
    report_folder = root + ("buck-out/bin/app/__amm_app_preview_%s_split_zip_report__/" % target)
    module_maps = find_all_plugin_properties(root)

    for textfile in os.listdir(report_folder):
    	if os.path.isfile(os.path.join(report_folder, textfile)):
    		size, method_num = calc_size(os.path.join(report_folder, textfile))
    		wording = "%s: %s size:\t\t %dK" %(TAG, textfile[:-len(".jar.txt")], size)
    		print wording

    size_dict, method_dict = calc_plugin_module_size(os.path.join(report_folder, "com.tencent.mm.plugin.mutidex.jar.txt"), module_maps)
    for name, size in size_dict.iteritems():
       print TAG + "Module %s,\t\tsize %dK" % (name, size)
