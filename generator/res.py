#!/usr/bin/python
from eclipse2buck import decorator
import os
from eclipse2buck.util import util
from eclipse2buck import config

from eclipse2buck.generator.base_target import BaseTarget
from eclipse2buck.util.calc_all_deps import DepsCalculator

class Resource(BaseTarget):
    is_res_existed = False
    is_assets_existed = False

    """
    gen resource target script
    Args:
      root(stnr): the APP root project's path
      name(str): the target's name
      
    Attributes:
      is_res_existed(bool): whether the res folder existed
      is_assets_existed(bool): whether the assets folder existed
    """    
    def __init__(self, root, name):
        BaseTarget.__init__(self, root, name, config.res_suffix)
        
        calc = DepsCalculator(root, name)
        mdeps = []
        for dep in calc.get_deps(name):
            if calc.is_res_existed[dep]:
                mdeps.append(dep)
        
        self.format_res_deps(mdeps)
        self.is_assets_existed = self.check_assets_existed(self.lib_path)
        #self.is_res_existed = self.check_res_existed(self.lib_path)
        self.is_res_existed = calc.is_res_existed[name]

        #always exported self
        if self.is_res_existed:
            self.exported_deps.append(":%s" % self.target_name(name))

#    def check_res_existed(self, path):
#        return os.path.isdir(os.path.join(path, "res")) and len(util.find_all_files_with_suffix(os.path.join(path, "res"), "*.*")) > 0

    def check_assets_existed(self, path):
        return os.path.isdir(os.path.join(path, "assets")) and len(util.find_all_files_with_suffix(os.path.join(path, "assets"), "*.*")) > 0

    def dump(self):
        if (not self.is_res_existed) and self.is_assets_existed:
            raise Exception("[%s]ONLY HAS ASSET??? PLZ PUT IT TO MAIN PROJECT" % self.target_name(self.proj_name))
        if self.is_res_existed:
            self._dump()
        
    @decorator.target("android_resource")
    def _dump(self):
        print "name = '%s'," % self.target_name(self.proj_name)
        print "package = '%s'," % config.package
        if self.is_res_existed:
            print "res = 'res',"
        if self.is_assets_existed:
            print "assets = 'assets',"
        print "visibility = [ 'PUBLIC' ],"
        self.gen_deps(self.deps)

    def format_res_deps(self, deps):
        """
        transfer project dependece to resource dependece
        Args:
          deps(list of str): the depencey project list
        """
        for dep in deps:
            dep_name = "//%s:%s%s" % (dep, dep, config.res_suffix)
            self.deps.append(dep_name)
