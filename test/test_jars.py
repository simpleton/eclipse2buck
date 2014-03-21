#!/usr/bin/python

from gen_jars import Jars

if __name__ == "__main__":
    jar = Jars('../', 'libnetscene')
    jar.dump()
    print jar.deps, jar.exported_deps
