#!/usr/bin/python
from gen_base_target import BaseTarget
import decorator
import util
import os

class NativeLib(BaseTarget):
    """
    gen native lib target
    """
    def __init__(self, root, name):
        BaseTarget.__init__(self, root, name, "_NATIVE")
        
    def dump(self):
        if self._is_exist_native():
            name = self.target_name(self.proj_name)
            self.gen_native_lib(name)
            self.deps.append(name)
    

    @decorator.target("prebuilt_native_library")
    def gen_native_lib(self, name):
        print "name = '%s'," % name
        print "native_libs = 'libs',"

    def _is_exist_native(self):
        native_lib_path = os.path.join(self.lib_path, "libs")
        return os.path.isdir(native_lib_path) and len(util.find_all_files_with_suffix(native_lib_path, "*.so")) > 0
