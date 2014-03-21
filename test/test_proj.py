#!/usr/bin/python

from eclipse2buck.generator.project import LibProject

if __name__ == "__main__":
    proj = LibProject("./", "libmmui")
    proj.dump()


