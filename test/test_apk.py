#!/usr/bin/python

from eclipse2buck.generator.create_apk import CreateApk

if __name__ == "__main__":
    p = CreateApk('./', 'app')
    p.dump()
