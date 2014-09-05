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


So, basically XDR describes a sequence of 4-byte blocks,
where each block is a serialization of some data type to
big-endian binary format.


--[prerequisites: ONC RPC]--

Now that it is clear how to build binary blocks, let's
see what are the sequence of binary data used in NFS.
For simplicity I call every sent or received block a
message.

NFS is based on ONC RPC, so every NFS message is also
ONC RPC message. The relation between XDR, ONC RPC and
NFS is:

  - XDR describes data types, binary represenatation
    for each type and how to combine them together
  - ONC RPC combines data types to form binary messages
    for sending requests (calls) and reading replies
  - NFS defines messages to do its stuff

Or in comparison with Python is the following:

  - XDR is like text file format (in which .py files
    are written)
  - ONC RPC is the description of Python language
    itself (how to define a function, how to pass params)
  - NFS is actual Python program

https://tools.ietf.org/html/rfc1057


--[NFS v2]--

There is no NFS version 1, because it was closed alpha.

https://tools.ietf.org/html/rfc1094

