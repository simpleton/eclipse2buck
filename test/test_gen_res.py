#!/usr/bin/python

from eclipse2buck.generator.res import Resource

if __name__ == "__main__":
    p = Resource('./', 'libmmui')
    p.dump()



