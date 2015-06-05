"""
Call function from standard C library.

ABI (binary, C compiler is not needed), inline (no build step)

"""

from cffi import FFI

import cffi
print "CFFI v%s" % cffi.__version__


# --- describe C interface

ffi = FFI()
ffi.cdef("""
     int printf(const char *format, ...);
""")

# --- load libraries

# this loads standard library for C (Unix convention)
cstdlib = ffi.dlopen(None)


# --- prepare arguments and call described functions

arg = ffi.new("char[]", "world")
numchars = cstdlib.printf("hi there, %s!\n", arg)
print numchars
