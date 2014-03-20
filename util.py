import os
import fnmatch
import decorator

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
    
