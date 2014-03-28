#!/usr/bin/python
import os
import sys
from eclipse2buck.util.config_file_parser import ProjectPropertiesParser
from eclipse2buck.util import util

class DepsCalculator:
    deps_dict = {}
    is_res_existed = {}
    root = ""
    """
    calculate all deps projects list. In eclipse, all deps relationship is exported, so we want the whole list of deps project. we deep in all the deps project until the project without any dependency.
    """
    def __init__(self, root, current):
        self.root = root
        if self.is_android_lib_proj(current):
            if current not in self.is_res_existed.keys():
                self.is_res_existed[current] = self.check_res_existed(current)
            parser = ProjectPropertiesParser(os.path.join(root, current))
            deps = parser.deps
            self.deps_dict[current] = []
            for dep in deps:
                if dep in self.deps_dict.keys():
                    self.deps_dict[current].extend(self.deps_dict[dep])
                self.access_proj(dep, self.deps_dict[current])
        
    def is_android_lib_proj(self,folder):
        return os.path.isdir(folder) and not folder.startswith('.') and os.path.isfile(os.path.join(folder, 'project.properties'))
        
    def check_res_existed(self, path):
        return os.path.isdir(os.path.join(path, "res")) and len(util.find_all_files_with_suffix(os.path.join(path, "res"), "*.*")) > 0

    def access_proj(self, proj, deps):
        if proj not in deps:
            deps.append(proj)
        if proj not in self.is_res_existed.keys():
            self.is_res_existed[proj] = self.check_res_existed(proj)

        parser = ProjectPropertiesParser(os.path.join(self.root, proj))
        for dep in parser.deps:
            self.access_proj(dep, deps)
    
    def get_deps(self, current):
        return list(set(self.deps_dict[current]))

if __name__ == '__main__':
    mroot = sys.argv[1]
    mcurrent = sys.argv[2]
    calc = DepsCalculator(mroot, mcurrent)
    print calc.get_deps(mcurrent)
