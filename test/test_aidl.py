#!/usr/bin/python

from gen_aidl import AIDL

if __name__ == "__main__":
    aidl = AIDL('../', 'libnetscene')
    aidl.dump()
    aidl.dump_src()
