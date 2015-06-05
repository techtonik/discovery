"""
Call function from WINAPI.

ABI (binary, C compiler is not needed), inline (no build step)

"""

from cffi import FFI

import cffi
print "CFFI v%s" % cffi.__version__


# --- describe C interface

ffi = FFI()
ffi.cdef("""
    DWORD GetTickCount(void);
""")


# --- load libraries

C = ffi.dlopen("kernel32.dll")


# --- prepare arguments and call described functions

p = C.GetTickCount()
print "GetTickCount: %s %s" % (p, type(p))
