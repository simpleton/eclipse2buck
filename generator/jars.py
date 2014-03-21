#!/usr/bin/python

from eclipse2buck.generator.base_target import BaseTarget
from eclipse2buck import  decorator
from eclipse2buck.util import util
import os
class Jars(BaseTarget):
    """
    generated all jar's targets
    """
    jar_list = []
    def __init__(self, root, name):
        BaseTarget.__init__(self, root, name, "_JAR")
        folder = self.lib_path
        self.jar_list = util.find_all_files_with_suffix(folder, "*.jar")
        for jar_path in self.jar_list:
            name = self.target_name(util.path_get_basename(jar_path))
            self.exported_deps.append(":%s" % name)

        
    @decorator.target("prebuilt_jar")
    def gen_jar(self, name, relative_path):
        print "name = '%s'," % name
        print "binary_jar = '%s'," % relative_path
        print "visibility = [ 'PUBLIC' ],"

    def dump(self):
        for jar_path in self.jar_list:
            name = self.target_name(util.path_get_basename(jar_path))
            self.gen_jar(name, jar_path)
