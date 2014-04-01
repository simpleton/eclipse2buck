#!/usr/bin/python

from eclipse2buck.generator.base_target import BaseTarget
from eclipse2buck.generator.jars import Jars
from eclipse2buck.generator.native import NativeLib
from eclipse2buck.generator.res import Resource
from eclipse2buck.generator.aidl import AIDL
from eclipse2buck.generator.project_config import ProjectConfig
from eclipse2buck.generator.create_apk import CreateApk
from eclipse2buck import decorator
from eclipse2buck.util import util
from eclipse2buck import config
import os
import sys

class LibProject(BaseTarget):
    aidl = None
    jar = None
    native = None
    res = None
    project_config = None
    """
    gen native lib target
    Vars:
      aidl:aidl_target
      jar: jar target
      native: native target
      res: resource target
    """
    def __init__(self, root, name, aidl, jar, native, res, project_config):
        BaseTarget.__init__(self, root, name, config.proj_suffix)
        self.aidl = aidl
        self.jar = jar
        self.native = native
        self.res = res
        self.project_config = project_config
        self.merge_all_deps()

    def __init__(self, root, name):
        BaseTarget.__init__(self, root, name, config.proj_suffix)
        self.res = Resource(root, name)
        self.aidl = AIDL(root, name)
        self.jar = Jars(root, name)
        self.native = NativeLib(root, name)
        self.project_config = ProjectConfig(root, name)
        self.merge_all_deps()

    def dump(self, *args):
        if len(args) == 0:
           self._dump()
        else:
            output_file = args[0]
            terminal = sys.stdout
            sys.stdout = open(output_file, 'w')
            self._dump()
            sys.stdout.close()
            sys.stdout = terminal

    def _dump(self):
         self.jar.dump()
         self.native.dump()
         self.aidl.dump()
         self.res.dump()
         self.project_config.dump()
         self.gen_android_lib()
         if self.proj_name == 'app':
             create_apk = CreateApk(self.root, self.proj_name)
             create_apk.dump()

    def merge_all_deps(self):
        src_exported_deps, src_deps = self.format_proj_deps()

        self.deps.extend(src_deps)
        self.deps.extend(self.aidl.deps)
#        self.deps.extend(self.res.deps)
        self.deps.extend(self.jar.deps)
        self.deps.extend(self.native.deps)

        self.exported_deps.extend(src_exported_deps)
        self.exported_deps.extend(self.aidl.exported_deps)
        self.exported_deps.extend(self.res.exported_deps)
        self.exported_deps.extend(self.jar.exported_deps)
        self.exported_deps.extend(self.native.exported_deps)

    def print_all_java(self, folders):
        content = ""
        for folder in folders:
            content += ("'%s/**/*.java'," % folder)
        return content
        

    @decorator.target("android_library")
    def gen_android_lib(self):
        print "name = '%s'," % self.target_name(self.proj_name)
        print "android_target = '%s'," % self.properties.sdk_target
        
        ## get all folders that contained JAVA file
        folders = util.find_all_folder_contains_file_with_suffix(os.path.join(self.root, self.proj_name), '*.java')
        ##ignore bin folder
        if 'bin' in folders:
            folders.remove('bin')
        ##print srcs target
        print "srcs = glob([%s])" % self.print_all_java(folders)

        ##append genfile(*.aidl)
        if self.aidl.is_existed_aidl():
            print "+ ["
            self.aidl.dump_src()
            print "]"
        print ","

        print "visibility = [ 'PUBLIC' ],"
        print "manifest = 'AndroidManifest.xml',"

        self.gen_deps(self.deps)
        self.gen_exported_deps(self.exported_deps)
    

    def format_proj_deps(self):
        deps = []
        export_deps = []
        for proj in self.properties.deps:
            target = "//%s:%s" % (proj, self.target_name(proj))
            export_deps.append(target)
        return export_deps, deps

if __name__ == "__main__":

    if len(sys.argv) > 2:
        root_path = sys.argv[1]
        target_project = sys.argv[2]
        proj = LibProject(root_path, target_project)
        proj.dump('tmp')
        proj.dump()
    else:
        print """
        Plz pass two arguments: 
        1.the root folder of the app project 
        2.the target lib folder
        just like:
          python -m eclipse2buck.generator.project ./ libmmui
        """
   

