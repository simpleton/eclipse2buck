#!/usr/bin/python

from gen_native import NativeLib

if __name__ == "__main__":
    nativelib = NativeLib("../", "libnetscene")
    nativelib.dump()
    print nativelib.deps, nativelib.exported_deps
