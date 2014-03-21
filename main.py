#!/usr/bin/python

import sys, os
from eclipse2buck.generator.project import LibProject

def travell_folders(root, exclude_folder):
    for f in os.listdir(root):
        if f != exclude_folder and is_android_lib_proj(f):
            lib_proj = LibProject(root, f)
            lib_proj.dump(os.path.join(root, f, "BUCK"))
            

def is_android_lib_proj(folder):
    return os.path.isdir(folder) and not folder.startswith('.') and os.path.isfile(os.path.join(folder, 'project.properties'))

if __name__ == '__main__':
    if len(sys.argv) > 2:
        root_path = sys.argv[1]
        android_bin_path= sys.argv[2]
        travell_folders(root_path, android_bin_path)
    else:
        print """
        Plz pass two arguments:
        1. the root folder of the whole project
        2. the bin project of the whole project, we wouldn't support generator bin project's BUCK file.Just use the templeta, if woundn't change.
          python -m eclipse2buck.main ./ app        
        """

