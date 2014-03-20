import decorator
import os
import util
import config

from gen_base_target import BaseTarget

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
        BaseTarget.__init__(self, root, name, "_res")
        self.format_res_deps(self.properties.deps)
        self.is_assets_existed = self.check_assets_existed(self.lib_path)
        self.is_res_existed = self.check_res_existed(self.lib_path)

        #always exported self
        self.exported_deps.append(":%s%s" % (name, self._suffix))

    def check_res_existed(self, path):
        return os.path.isdir(os.path.join(path, "res")) and len(util.find_all_files_with_suffix(os.path.join(path, "res"), "*.*")) > 0

    def check_assets_existed(self, path):
        return os.path.isdir(os.path.join(path, "assets")) and len(util.find_all_files_with_suffix(os.path.join(path, "assets"), "*.*")) > 0

    def dump(self):
        if (not self.is_res_existed) and self.is_assets_existed:
            raise Exception("ONLY HAS ASSET??? PLZ PUT IT TO MAIN PROJECT")
        if self.is_res_existed:
            self._dump()
        
    @decorator.target("android_resource")
    def _dump(self):
        print "name = '%s%s'," % (self.proj_name, self._suffix)
        print "package = '%s'," % config.package
        if self.is_res_existed:
            print "res = 'res',"
        if self.is_assets_existed:
            print "assets = 'assets',"
        print "visibility = [ 'PUBLIC' ],"
        util.gen_deps(self.deps)

