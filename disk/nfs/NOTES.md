--[prerequisites: XDR]--

NFS protocol is based on XDR description, which has
the following properties:

 * "..byte is defined as 8 bits of data.."
 * basic block size is 4 bytes big endian
   (0xAABBCCDD  is recorded as AA BB CC DD in memory)

http://tools.ietf.org/html/rfc4506


Integer
 C: int identifier;
    4 bytes, [-2147483648,2147483647], two's complement
 C: unsigned int identifier;
    4 bytes, [0,4294967295]
 C: hyper identifier;
    unsigned hyper identifier;
    8 bytes, 

Enumeration
 C: enum { name-identifier = constant, ... } identifier;
    enum { RED = 2, YELLOW = 3, BLUE = 5 } colors;
    4 bytes, [selected integers], two's complement

Boolean
 C: bool identifier;
    enum { FALSE = 0, TRUE = 1 } identifier;
    4 bytes, 00000000 or 00000001
    
Floating-Point
 C: float identifier;
    4 bytes, SEF (Sign1, Exp2nent8, Frac2tional23 = 32)
             exp=127 is zero point

    https://en.wikipedia.org/wiki/Single-precision_floating-point_format#IEEE_754_single-precision_binary_floating-point_format:_binary32
...


Let's better see which XDR types are really used in NFS.

