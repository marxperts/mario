#!/usr/bin/env python3
import sys, os, platform
from cffi import FFI
V = sys.version_info[:3]

# print("Platform: {}".format(platform.system()))
# print("Python  : {}".format(V))

ffibuilder = FFI()

# Is this script called from local directory or master directory?"
if  os.path.isfile("marpck.h"):
    pre=""
    ioinc  = "-I."
    sotarget = './_libmar345.{}.{}.so'.format(platform.system(),platform.machine())
else:
    pre="C/"
    ioinc  = "-IC"
    sotarget = 'lib/_libmar345.{}.{}.so'.format(platform.system(),platform.machine())

with open(pre+"marpck.h") as f:
    ffibuilder.cdef(f.read())

ffibuilder.set_source(
    "_libmar345", """
    #include "marpck.h"
    """,
	sources=[pre+'marpck.c'],
    extra_compile_args=['-g', '-fPIC']
)
ffibuilder.compile(verbose=True, target=sotarget)


if __name__ == "__main__":
    if platform.system() == "Darwin":
        sotarget = "../mario/_libmar345.cpython-{}{}-darwin.so".format( V[0], V[1])
    elif platform.system() == "Windows":
        sotarget = "../mario/_libmar345.pyd"
    else:
        sotarget = "../mario/_libmar345.so"
    print("Shared library: {}".format(sotarget))
    ffibuilder.compile(verbose=True, target=sotarget)
