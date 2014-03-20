import decorator
import os
import util
import config
from config_file_parser import Project_properties_parser

class Resource:
    name = ''
    deps = []
    root = ''
    is_res_existed = False
    is_assets_existed = False
    _exported_deps = []
    _res_suffix = "_res"
    _lib_path = ''
    """
    gen resource target script
    Args:
      root(stnr): the APP root project's path
      name(str): the target's name

    Attributes:
      name(str): the target's name
      root(str): the APP root project's path
      is_res_existed(bool): whether the res folder existed
      is_assets_existed(bool): whether the assets folder existed
      deps(list of str): the dependence module list of this target
      exproted_deps(list of str): the expored dependency module list
    """    
    def __init__(self, root, name):
        self.name = name
        self.root = root
        self._lib_path = os.path.join(self.root, self.name)
        properties = Project_properties_parser(self._lib_path)
        self.format_res_deps(properties.deps)

        self.is_assets_existed = self.check_assets_existed(self._lib_path)
        self.is_res_existed = self.check_res_existed(self._lib_path)

        #always exported self
        self._exported_deps.append(":%s%s" % (name, self._res_suffix))

    def check_res_existed(self, path):
        return os.path.isdir(os.path.join(path, "res")) and len(util.find_all_files_with_suffix(os.path.join(path, "res"), "*.*")) > 0

    def check_assets_existed(self, path):
        return os.path.isdir(os.path.join(path, "assets")) and len(util.find_all_files_with_suffix(os.path.join(path, "assets"), "*.*")) > 0

    def format_res_deps(self, deps):
        """
        transfer project dependece to resource dependece
        Args:
          deps(list of str): the depencey project list
        """
        for dep in deps:
            dep_name = "//%s:%s%s" % (dep, dep, self._res_suffix)
            self.deps.append(dep_name)

    def dump(self):
        if (not self.is_res_existed) and self.is_assets_existed:
            raise Exception("ONLY HAS ASSET??? PLZ PUT IT TO MAIN PROJECT")
        if self.is_res_existed:
            self._dump()
        
    @decorator.target("android_resource")
    def _dump(self):
        print "name = '%s%s'," % (self.name, self._res_suffix)
        print "package = '%s'," % config.package
        if self.is_res_existed:
            print "res = 'res',"
        if self.is_assets_existed:
            print "assets = 'assets',"
        print "visibility = [ 'PUBLIC' ],"
        util.gen_deps(self.deps)

