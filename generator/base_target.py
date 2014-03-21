#!/usr/bin/python
import os
from eclipse2buck.util.config_file_parser import ProjectPropertiesParser
from eclipse2buck.decorator import var_with_comma

class BaseTarget:
    proj_name = ""
    root = ""
    properties = None
    lib_path = ""
    deps = []
    exported_deps = []
    _suffix = ""
    """
    Base class for gen target class
    Args:
      root(stnr): the APP root project's path
      name(str): the target's name
      suffix(str): the suffix for target

    Attributes:
      name(str): the target's name
      root(str): the APP root project's path
      deps(list of str): the dependence module list of this target
      exproted_deps(list of str): the expored dependency module list
      properties(Project_properties_parser): the eclipse project properties info
      lib_path(str): the library's path
    """    
    def __init__(self, root, name, suffix):
        self.root = root
        self.proj_name = name
        self._suffix = suffix
        self.lib_path = os.path.join(root, name)
        self.properties = ProjectPropertiesParser(self.lib_path)
        self.deps = []
        self.exported_deps = []

    def target_name(self, name):
        """
        Returns:
          str: buck target's name
        """
        return "%s%s" % (name, self._suffix)


    @var_with_comma("deps")
    def gen_deps(self, deps):
        for dep in deps:
            print "'%s'," % dep

    @var_with_comma("exported_deps")
    def gen_exported_deps(self, exported_deps):
        for dep in exported_deps:
            print "'%s'," % dep
