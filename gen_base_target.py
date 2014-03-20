import os
from config_file_parser import Project_properties_parser

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
        self.properties = Project_properties_parser(self.lib_path)
    
    def format_res_deps(self, deps):
        """
        transfer project dependece to resource dependece
        Args:
          deps(list of str): the depencey project list
        """
        for dep in deps:
            dep_name = "//%s:%s%s" % (dep, dep, self._suffix)
            self.deps.append(dep_name)
