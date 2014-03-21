#!/usr/bin/python

from eclipse2buck.generator import aidl

if __name__ == "__main__":
    aidl = aidl.AIDL('./', 'libnetscene')
    aidl.dump()
    aidl.dump_src()
