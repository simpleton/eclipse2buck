#!/usr/bin/python

from gen_lib_proj import LibProject

if __name__ == "__main__":
    proj = LibProject("../", "libnetscene")
    proj.dump()
