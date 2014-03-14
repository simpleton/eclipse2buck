import sys
import decorator
import fnmatch
import os
import glob

@decorator.target("android_resource")
def gen_android_res():
    print "hello"

@decorator.target("android_library")
def gen_android_lib(name, sdk_target, aidl):
    print "name = "

@decorator.target("prebuilt_native_library")
def gen_native_lib(name):
    print "name = '%s_native'" % name
    print ","
    print "native_libs = libs"
    print ","

@decorator.target("gen_aidl")
def gen_aidl(name, aidl, proj):
    print "name = %s," % name[:-5]
    print "aidl = '%s'," % aidl
    print "import_path = '%s/src/'," % proj

def gen_aidls(aidls, proj):
    for aidl in aidls:
        name = os.path.split(aidl)[1]
        gen_aidl(name, aidl, proj)

def _print_manifest():
    print "manifest = 'AndroidManifest.xml'"
    print ","

def _print_visibility():
    print "visibility = [ 'PUBLIC' ]"
    print ","

def _print_defs(name):
    print "deps = DEPS + [ %s_res ]" % name
    print ","
    print "exported_deps = DEPS + [ %s_res ]" % name
    print ","

def _print_src(aidls):
    print "srcs = glob(['src/**/*.java', 'gen/**/*.java']) + "
    print "["
    _print_aidl_genfile(aidls)
    print "]"
    print ","

def _print_aidl_genfile(aidls):
    for aidl in aidls:
        #remove .aild
        aidl = aidl[:-5]
        print "genfile( '%s.java' )," % aidl

def _find_all_aidls(r):
    matches = []
    for root, dirnames, filenames in os.walk(r):
        for filename in fnmatch.filter(filenames, '*.aidl'):
            matches.append(os.path.relpath(os.path.join(root,filename), r))
    return matches

if __name__ == "__main__":
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = os.getcwd()
    root = os.path.realpath(root)
    path, proj_name = os.path.split(root)
    aidls = _find_all_aidls(root)
    gen_aidls(aidls, proj_name)

#    aidls =  _find_all_aidls(os.path.realpath("../libnetscene"))
#    _print_src(aidls)

