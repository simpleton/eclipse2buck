#!/usr/bin/python
from eclipse2buck import decorator
from eclipse2buck.generator.base_target import BaseTarget
from eclipse2buck import config

class ProjectConfig(BaseTarget):
    def __init__(self, root, name):
        BaseTarget.__init__(self, root, name, config.proj_suffix)

    @decorator.target("project_config")
    def dump(self):
        print ("src_target = ':%s'," % self.target_name(self.proj_name))
        """if self.proj_name == "libsupport":
            print "src_roots = ['src', 'java', 'eclair', 'eclair-mr1', 'froyo', 'gingerbread', 'honeycomb', 'honeycomb_mr2', 'ics', 'ics-mr1', 'jellybean', 'jellybean-mr1', 'jellybean-mr2'],"
        elif self.proj_name == "app":
            print "src_roots = [ 'src', 'gen', 'autogen' ],"
        else:
            print "src_roots = [ 'src', 'gen' ],"
        """
