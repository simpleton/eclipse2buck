import os

class Project_properties_parser:
    #use sdk 16 as default
    sdk_target = "16" 
    is_library = False
    deps = []

    def __init__(self, proj_path):
        properties_path = os.path.join(proj_path, "project.properties")
        self.sdk_target, self.library_flag, self.deps = self.parse(properties_path)

    def parse(self, project_properties_path):
        """
        parse the project.properties file
        Args:
          properties_properties_path(str): the properties file path
        Returns:
          sdk_target,
          library_flag,
          deps,
        """
        sdk_target = None
        lib_flag = None
        deps = []
        with open(project_properties_path) as fd:
            for line in fd.readlines():
                if (line.startswith("target=")):
                    sdk_target = line[len("target="):]
                    sdk_target = sdk_target.strip("\r\n")
                if (line.startswith("android.library=")):
                    lib_flag = line[len("android.library="):]
                    lib_flag = lib_flag.strip("\r\n")
                if (line.startswith("android.library.reference.")):
                    dep = line.split('=')[1].strip("\r\n")
                    if (dep.startswith("../")):
                        dep = dep[3:]
                    deps.append(dep)
        return sdk_target, lib_flag, deps
    
    

    
