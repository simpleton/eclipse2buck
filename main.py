#!/usr/bin/python

import sys, os
from eclipse2buck.generator.project import LibProject
from eclipse2buck import build_secondary_dex_list as gen_sec_dlist
from eclipse2buck import build_bin_dep_list as gen_dep

def travell_folders(root, bin_folder):
    for f in os.listdir(root):
        if f != bin_folder and is_android_lib_proj(f):
            lib_proj = LibProject(root, f)
            lib_proj.dump(os.path.join(root, f, "BUCK"))
            

def is_android_lib_proj(folder):
    return os.path.isdir(folder) and not folder.startswith('.') and os.path.isfile(os.path.join(folder, 'project.properties'))

if __name__ == '__main__':
    if len(sys.argv) > 2:
        root_path = sys.argv[1]
        bin_name= sys.argv[2]

        bin_path = os.path.join(root_path, bin_name)
        #gen bin's DEPS
        gen_dep.dump_binary_deps(bin_path, os.path.join(bin_path, 'DEFS'))
        #gen the list of secondary dex patterns
        gen_sec_dlist.dump_secondary_pattern(root_path, os.path.join(bin_path, 'SECONDARY_DEX_PATTERN_LIST'))
        #gen all libs' BUCK files
        travell_folders(root_path, bin_name)
    else:
        print """
        Plz pass two arguments:
        1. the root folder of the whole project
        2. the bin project of the whole project, we wouldn't support generator bin project's BUCK file.Just use the templeta, if woundn't change.
          python -m eclipse2buck.main ./ app        
        """

