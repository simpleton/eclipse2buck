from gen_base_target import BaseTarget
from gen_jars import Jars
from gen_native import NativeLib
from gen_res import Resource
from gen_aidl import AIDL
import decorator
import util
import os

class LibProject(BaseTarget):
    aidl = None
    jar = None
    native = None
    res = None
    """
    gen native lib target
    Vars:
      aidl:aidl_target
      jar: jar target
      native: native target
      res: resource target
    """
    def __init__(self, root, name, aidl, jar, native, res):
        BaseTarget.__init__(self, root, name, "_PROJ")
        self.aidl = aidl
        self.jar = jar
        self.native = native
        self.res = res
        self.merge_all_deps()

    def __init__(self, root, name):
        BaseTarget.__init__(self, root, name, "_PROJ")
        self.aidl = AIDL(root, name)
        self.jar = Jars(root, name)
        self.native = NativeLib(root, name)
        self.res = Resource(root, name)
        self.merge_all_deps()

    def dump(self):
        self.jar.dump()
        self.native.dump()
        self.aidl.dump()
        self.res.dump()
        self.gen_android_lib()

    def merge_all_deps(self):
        self.deps.extend(self.aidl.deps)
        self.deps.extend(self.res.deps)
        self.deps.extend(self.jar.deps)
        self.deps.extend(self.native.deps)

        self.exported_deps.extend(self.aidl.exported_deps)
        self.exported_deps.extend(self.res.exported_deps)
        self.exported_deps.extend(self.jar.exported_deps)
        self.exported_deps.extend(self.native.exported_deps)

    @decorator.target("android_library")
    def gen_android_lib(self):
        print "name = '%s'," % self.target_name(self.proj_name)
        
        if not self.properties.sdk_target.startswith("Google"):
            sdk_target = "Google Inc.:Google APIs:%s" % self.properties.sdk_target.split('-')[1]
        print "android_target = '%s'," % sdk_target

        ##print srcs target
        if self.proj_name == "libsupport":
            print "srcs = glob(['src/**/*.java', 'java/**/*.java', 'eclair/**/*.java','eclair-mr1/**/*.java', 'froyo/**/*.java', 'gingerbread/**/*.java','honeycomb/**/*.java', 'honeycomb_mr2/**/*.java', 'ics/**/*.java', 'ics-mr1/**/*.java', 'jellybean/**/*.java', 'jellybean-mr1/**/*.java', 'jellybean-mr2/**/*.java']) + ",
        else:
            print "srcs = glob(['src/**/*.java', 'gen/**/*.java'])"
        if self.aidl.is_existed_aidl():
            print "+ ["
            self.aidl.dump_src()
            print "]"
        print ","

        print "visibility = [ 'PUBLIC' ],"
        print "manifest = 'AndroidManifest.xml',"

        self.gen_deps(self.deps)
        self.gen_exported_deps(self.exported_deps)
    
