import decorator

@decorator.target("android_resource")
def gen_android_res():
    print "hello"

@decorator.target("android_library")
def gen_android_lib(name, sdk_target, aidl):
    print "name = "


def _print_manifest():
    print "manifest = 'AndroidManifest.xml',",

def _print_visibility():
    print "visibility = [ 'PUBLIC' ],"

if __name__ == "__main__":

    gen_res()
