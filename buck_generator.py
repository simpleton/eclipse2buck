import sys
import decorator
import fnmatch
import os
import glob

@decorator.target("android_resource")
def gen_android_res(name, deps, is_res, is_assets):
    export_deps = deps
    deps = deps
    name = name + "_res"
    print "name = '%s'," % name
    print "package = 'com.tencent.mm',"
    if is_res:
        print "res = 'res',"
    if is_assets:
        print "assets = 'assets',"
    print "visibility = [ 'PUBLIC' ],"
    gen_deps(deps)
    export_deps.append(name)
    deps.append(name)
    return export_deps, deps

@decorator.target("android_library")
def gen_android_lib(name, sdk_target, aidl, deps, export_deps):
    name = name + "_proj"
    print "name = '%s'," % name
    print "android_target = '%s'," % sdk_target
    ##print srcs target
    print "srcs = glob(['src/**/*.java', 'gen/**/*.java']) + "
    print "["
    _print_aidl_genfile(aidls)
    print "],"

    print "visibility = [ 'PUBLIC' ],"
    print "manifest = 'AndroidManifest.xml',"

    gen_deps(deps)
    gen_export_deps(export_deps)

@decorator.target("prebuilt_native_library")
def gen_native_lib(name):
    native_name = name + "_native"
    print "name = '%s'," % native_name
    print "native_libs = libs,"
    return native_name

@decorator.target("gen_aidl")
def gen_aidl(name, aidl, proj):
    name = name[:-5]
    print "name = '%s'," % name
    print "aidl = '%s'," % aidl
    print "import_path = '%s/src/'," % proj
    return name

@decorator.target("prebuilt_jar")
def gen_jar(name, relative_path):
    print "name = '%s'," % name
    print "binary_jar = '%s'," % relative_path
    print "visibility = [ 'PUBLIC' ],"
    return name

@decorator.var_with_comma("deps")
def gen_deps(deps):
    for dep in deps:
        print ":%s," % dep


@decorator.var_with_comma("exported_deps")
def gen_exported_deps(exported_deps):
    for dep in exported_deps:
        print ":%s," % target

def gen_res(path, name, deps):
    is_res = False
    is_assets = False
    if len(_find_all_files_with_suffix(path + "/res", "*.xml")) > 0:
        is_assets = True
    if len(os.listdir(path + "/assets")) > 0:
        is_assets = True
    if is_res or is_assets:
        return gen_android_res(name, deps, is_res, is_assets)


def gen_jars(path):
    export_deps = []
    deps = []
    jars = _find_all_files_with_suffix(path, "*.jar")
    for relative_path in jars:
        ##extract filename without suffix (-4 means .jar's lenght)
        name = relative_path.split("/")[-1][:-4]
        target = gen_jar(name, relative_path)
        export_deps.append(target)
        deps.append(target)
    return  export_deps, deps

def gen_aidls(aidls, proj):
    export_deps = []
    deps = []
    for aidl in aidls:
        name = os.path.split(aidl)[1]
        target = gen_aidl(name, aidl, proj)
        deps.append(target)
    return export_deps, deps

def gen_native_libs(path, name):
    export_desp = []
    deps = []
    if len(os.listdir(path + "/libs")) > 0:
        target = gen_native_lib(name)
        export_desp.append(target)
        deps.append(target)
    return export_desp, deps

def _print_aidl_genfile(aidls):
    for aidl in aidls:
        #remove .aild
        aidl = aidl[:-5]
        print "genfile( '%s.java' )," % aidl

def _find_all_aidls(relative_path):
    return _find_all_files_with_suffix(relative_path, "*.aidl")

def _find_all_files_with_suffix(relative_path, suffix):
    matches = []
    for root, dirnames, filenames in os.walk(relative_path):
        for filename in fnmatch.filter(filenames, suffix):
            matches.append(os.path.relpath(os.path.join(root,filename), relative_path))
    return matches

def parse_deps(path):
    proj_fd = path + "/project.properties"
    sdk_target = None
    lib_flag = None
    deps = []
    with open(proj_fd) as fd:
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
        
        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = os.getcwd()
    root = os.path.realpath(root)
    path, proj_name = os.path.split(root)
    ##gen aidls
    aidls = _find_all_aidls(root)
    #gen_aidls(aidls, proj_name)
    ##gen libs
    #print gen_libs(root, proj_name)
#    aidls =  _find_all_aidls(os.path.realpath("../libnetscene"))
#    _print_src(aidls)
    #print gen_jars(root)
    #print gen_android_res(proj_name,)
    print parse_deps(root)
