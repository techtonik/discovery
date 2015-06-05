"""
Call function from standard C library.

ABI (binary, C compiler is not needed), outbound (build step)

Run me after 002cffi_ABI_outbound_build.py
"""

# this import is build in the first phase
from _cffi_ABI_outbound_generated import ffi


# --- load libraries

import sys
if sys.platform != 'win32':
  # this loads standard library for C (Unix convention)
  lib = ffi.dlopen(None)
else:
  # on windows CFFI fails to load C stdlib in this mode,
  # so finding it manually
  import ctypes.util
  lib = ffi.dlopen(ctypes.util.find_library("c"))


# --- prepare arguments and call described functions

lib.printf("hi there, %s!\n", ffi.new("char[]", "world"))
