from gen_base_target import BaseTarget
import decorator
import util

class AIDL(BaseTarget):
    """
    generated all aidl targets
    """
    aidl_path_list = []
    def __init__(self, root, name):
        BaseTarget.__init__(self, root, name, "_AIDL")
        self.aidl_path_list = self._find_all_aidls(self.lib_path)

    def dump_src(self):
        for aidl in self.aidl_path_list:
            #remove .aild
            aidl = aidl[:-5]
            print "genfile( '%s.java' )," % aidl
    
    def dump(self):
        for aidl_path in self.aidl_path_list:
            name = util.path_get_basename(aidl_path)
            self.deps.append(self._gen_aidl_target(name, aidl_path))
            
    def _find_all_aidls(self, relative_path):
        path_list = util.find_all_files_with_suffix(relative_path, "*.aidl") 
        exclude_aidls = ["src/com/tencent/mm/cache/MCacheItem.aidl",
                         "src/com/tencent/tmassistantsdk/downloadclient/TMAssistantDownloadTaskInfo.aidl"]
        #some aidl file needn't be generated
        for exclude_aidl in exclude_aidls:
            if exclude_aidl in path_list:
                path_list.remove(exclude_aidl)

        return path_list

    @decorator.target("gen_aidl")
    def _gen_aidl_target(self, aidl_name, path):
        """
        print the aidl target 
        Returns:
          str: the target name which lib target should depend on
        """
        print "name = '%s'," % aidl_name
        print "aidl = '%s'," % path
        print "import_path = '%s/src/'," % self.proj_name
        return ":%s" % aidl_name