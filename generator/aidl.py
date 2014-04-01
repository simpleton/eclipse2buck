#!/usr/bin/python

from eclipse2buck.generator.base_target import BaseTarget
from eclipse2buck.decorator import target
from eclipse2buck.util import util
from eclipse2buck import config
import os

class AIDL(BaseTarget):
    """
    generated all aidl targets
    Note:
      we comsume all aidl contains in src folder
    """
    aidl_path_list = []
    def __init__(self, root, name):
        BaseTarget.__init__(self, root, name, config.aidl_suffix)
        self.aidl_path_list = self._find_all_aidls(os.path.join(self.lib_path, 'src'))
        for aidl_path in self.aidl_path_list:
            name = self.target_name(util.path_get_basename(aidl_path))
            self.deps.append(":%s" % name)

    def dump_src(self):
        for aidl in self.aidl_path_list:
            #remove .aild
            aidl = aidl[:-5]
            print "genfile( '%s.java' )," % aidl
    
    def dump(self):
        for aidl_path in self.aidl_path_list:
            name = self.target_name(util.path_get_basename(aidl_path))
            self._gen_aidl_target(name, aidl_path)

    def is_existed_aidl(self):
        return len(self.aidl_path_list) > 0


    def _find_all_aidls(self, relative_path):
        path_list = util.find_all_files_with_suffix(relative_path, "*.aidl") 

        #some aidl file needn't be generated
        path_list_with_src = []
        for path in path_list:
            if self.is_only_parcelbale(path):
                path_list_with_src.append(os.path.join('src', path))

        return path_list_with_src

    def is_only_parcelbale(self, file):
        has_useful_content = False
        with open(os.path.join(self.proj_name, 'src', file), 'r') as infile:
            lines = infile.read().splitlines()
            for line in lines:
                if line.startswith("interface"):
                    has_useful_content = True
                    break
        return has_useful_content


    @target("gen_aidl")
    def _gen_aidl_target(self, aidl_name, path):
        """
        print the aidl target 
        Returns:
          str: the target name which lib target should depend on
        """
        print "name = '%s'," % aidl_name
        print "aidl = '%s'," % path
        print "import_path = '%s/src/'," % self.proj_name

