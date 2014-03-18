import sys
import decorator
import fnmatch
import os
import glob

@decorator.target("android_resource")
def gen_android_res(name, in_deps, is_res, is_assets):
    export_deps = []
    deps = []
    name = name + "_res"
    print "name = '%s'," % name
    print "package = 'com.tencent.mm',"
    if is_res:
        print "res = 'res',"
    if is_assets:
        print "assets = 'assets',"
    print "visibility = [ 'PUBLIC' ],"
    gen_deps(in_deps)

    target = ":%s" % name
    export_deps.append(target)
    #deps.append(target)
    return export_deps, deps

@decorator.target("android_library")
def gen_android_lib(name, sdk_target, aidl, deps, export_deps):
    name = name + "_src"
    print "name = '%s'," % name
    #print "android_target = '%s'," % sdk_target

    ##print srcs target
    if name.startswith("libsupport"):
        print "srcs = glob(['src/**/*.java', 'java/**/*.java', 'eclair/**/*.java','eclair-mr1/**/*.java', 'froyo/**/*.java', 'gingerbread/**/*.java','honeycomb/**/*.java', 'honeycomb_mr2/**/*.java', 'ics/**/*.java', 'ics-mr1/**/*.java', 'jellybean/**/*.java', 'jellybean-mr1/**/*.java', 'jellybean-mr2/**/*.java']) + ",
    else:
        print "srcs = glob(['src/**/*.java', 'gen/**/*.java']) + "
    print "["
    _print_aidl_genfile(aidls)
    print "],"

    print "visibility = [ 'PUBLIC' ],"
    print "manifest = 'AndroidManifest.xml',"

    gen_deps(deps)
    gen_exported_deps(export_deps)

@decorator.target("prebuilt_native_library")
def gen_native_lib(name):
    native_name = name + "_native"
    print "name = '%s'," % native_name
    print "native_libs = 'libs',"
    return ":%s" % native_name

@decorator.target("gen_aidl")
def gen_aidl(name, aidl, proj):
    name = path_get_basename(name)
    print "name = '%s'," % name
    print "aidl = '%s'," % aidl
    print "import_path = '%s/src/'," % proj
    return ":%s" % name

@decorator.target("prebuilt_jar")
def gen_jar(name, relative_path):
    print "name = '%s'," % name
    print "binary_jar = '%s'," % relative_path
    print "visibility = [ 'PUBLIC' ],"
    return ":%s" % name

@decorator.var_with_comma("deps")
def gen_deps(deps):
    for dep in deps:
        print "'%s'," % dep

@decorator.var_with_comma("exported_deps")
def gen_exported_deps(exported_deps):
    for dep in exported_deps:
        print "'%s'," % dep

def gen_res(path, name, proj_deps):
    is_res, is_assets = check_res_stat(path)
    exported_deps, deps = format_res_deps(path, proj_deps)
    _exported_deps = []
    _deps = []
    if is_assets or is_res:
        _exported_deps, _deps = gen_android_res(name, deps, is_res, is_assets)
    return _exported_deps, _deps

def check_res_stat(path):
    return len(_find_all_files_with_suffix(os.path.join(path, "res"), "*.xml")) > 0, os.path.isdir(os.path.join(path, "assets")) and len(os.listdir(os.path.join(path, "assets"))) > 0

def check_res_existed(path):
    is_res, is_assets = check_res_stat(path)
    return is_res or is_assets

def gen_jars(path):
    export_deps = []
    deps = []
    jars = _find_all_files_with_suffix(path, "*.jar")
    for relative_path in jars:
        ##extract filename without suffix (-4 means .jar's lenght)
        name = relative_path.split("/")[-1][:-4]
        target = gen_jar(name, relative_path)
        export_deps.append(target)
        #deps.append(target)
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
    lib_path = os.path.join(path, "libs")
    if os.path.isdir(lib_path) and len(os.listdir(lib_path)) > 0:
        target = gen_native_lib(name)
        deps.append(target)
        #don't export native lib, buck will copy all native .so files
    return export_desp, deps

def _print_aidl_genfile(aidls):
    for aidl in aidls:
        #remove .aild
        aidl = aidl[:-5]
        print "genfile( '%s.java' )," % aidl

def _find_all_aidls(relative_path):
    aidls = _find_all_files_with_suffix(relative_path, "*.aidl") 
    no_aidls = ["src/com/tencent/mm/cache/MCacheItem.aidl",
               "src/com/tencent/tmassistantsdk/downloadclient/TMAssistantDownloadTaskInfo.aidl"]

    for no_aidl in no_aidls:
        if no_aidl in aidls:
            aidls.remove(no_aidl)

    return aidls
    

def _find_all_files_with_suffix(relative_path, suffix):
    matches = []
    for root, dirnames, filenames in os.walk(relative_path):
        for filename in fnmatch.filter(filenames, suffix):
            matches.append(os.path.relpath(os.path.join(root,filename), relative_path))
    return matches

def parse_deps(path):
    """
    parse the project propertie file,
    return (sdk_target, is_library_flag , deps)
    """
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
        
def format_proj_deps(root, folders):
    deps = []
    export_deps = []
    for proj in folders:
        target = "//%s:%s_src" % (proj, proj)
        #deps.append(target)
        export_deps.append(target)
    return export_deps, deps

def format_res_deps(root, folders):
    deps = []
    export_deps = []
    for proj in folders:
        target = "//%s:%s_src" % (proj, proj)
        deps.append(target)
        #export_deps.append(target)

    return export_deps, deps


def path_get_parent(path):
    return os.path.abspath(os.path.join(path, os.pardir))

def path_get_basename(path):
    return os.path.splitext(os.path.basename(path))[0]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = os.getcwd()
    root = os.path.realpath(root)
    path, proj_name = os.path.split(root)
    ##gen aidls
    aidls = _find_all_aidls(root)
    aidl_exported_deps, aidl_deps = gen_aidls(aidls, proj_name)
    ##gen native libs
    native_expoted_deps , native_deps = gen_native_libs(root, proj_name)
    ##gen jars
    jar_exported_deps, jar_deps = gen_jars(root)

    ##dep_libs just the folders of the dependency modules
    sdk_target, is_lib, dep_libs = parse_deps(root)
    proj_exported_deps, proj_deps = format_proj_deps(root, dep_libs)

    ##gen res
    res_exported_deps, res_deps = gen_res(root, proj_name, dep_libs)

    ##gen lib project
    all_deps = []
    all_deps.extend(proj_deps)
    all_deps.extend(res_deps)
    all_deps.extend(aidl_deps)
    all_deps.extend(native_deps)
    all_deps.extend(jar_deps)
    all_exported_deps = []
    all_exported_deps.extend(proj_exported_deps)
    all_exported_deps.extend(res_exported_deps)
    all_exported_deps.extend(aidl_exported_deps)
    all_exported_deps.extend(native_expoted_deps)
    all_exported_deps.extend(jar_exported_deps)

    gen_android_lib(proj_name, sdk_target, aidls, all_deps, all_exported_deps)
