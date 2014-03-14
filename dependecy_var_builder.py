import sys
import os
import var_name_decorate

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

@var_name_decorate.print_var
def write_binary_deps(var_name, root):
    deps = get_reference_lists(root)
    for dep in deps:
        print "'//" + dep + ":"+ dep + "_lib',"

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

    #var_name = (get_current_dep_name(root).split("/"))[-1] + "_DEPS"
    var_name = "DEPS"
    write_binary_deps(var_name, root)
