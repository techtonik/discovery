"""
Call function from standard C library.

ABI (binary, C compiler is not needed), outbound (build step)

Run me first to build importable _cffi_ABI_outbound_generated.py
"""

from cffi import FFI


# --- describe C interface

ffi = FFI()
ffi.cdef("""
     int printf(const char *format, ...);
""")


# --- set module name and build it

ffi.set_source('_cffi_ABI_outbound_generated', None)
print ffi.compile()
