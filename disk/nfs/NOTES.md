--[prerequisites: XDR]--

NFS protocol is based on XDR description, which is like
vintage Protocol Buffers. XDR has the following
properties:

 * "..byte is defined as 8 bits of data.."
 * basic block size is 4 bytes big endian
   (0xAABBCCDD  is recorded as AA BB CC DD in memory)
 * everything is composed out of basic blocks

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

Interesting things are `union` and `opaque` structures.

    opaque identifier[n];
    n mod 4 bytes

    opaque identifier<m>;
    4+4*m bytes

    opaque identifier<>;

`[n]` is fixed length of size n serialized as bytes with
padding zeroes at the end. `<m>` is variable buffer with
size m, with size int coming before buffer data. If size
is not specified, it is `(2**32) - 1`


--[prerequisites: ONC RPC]--

ONC RPC is a service on port UDP/TCP 111, which can
redirect clients to other ports.

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

ONC RPC has XDR definitions like this:

    enum reply_stat {
       MSG_ACCEPTED = 0,
       MSG_DENIED   = 1
    };

On binary level that means either 00000000 or 00000001,
so both field length and data for validation is included.
For API access, there are names `reply_stat` and MSG_*
constants.

--[ONC RPC: connecting]--

Build a message, send to port 111, read reply. Message
in XDR protol looks like this:

    struct rpc_msg {
       unsigned int xid;
       union switch (msg_type mtype) {
       case CALL:
          call_body cbody;
       case REPLY:
          reply_body rbody;
       } body;
    };

Where `msg_type` is:

    enum msg_type {
        CALL  = 0,
        REPLY = 1
    };

`xid` is some random number. `call_cbody` is nested
structure for the CALL message type (00000000):

    struct call_body {
       unsigned int rpcvers; /* must be equal to two (2) */
       unsigned int prog;
       unsigned int vers;
       unsigned int proc;
       opaque_auth cred;
       opaque_auth verf;
       /* procedure specific parameters start here */
    };

So, without `opaque_*` fields, the length of the message
so far is 4(xid)+4(mtype)+4(rpcvers)+4(prog)+4(vers)+
4(proc) = 6x4 = 24 bytes.

So, the "do nothing" call for NFS in binary form will
look like this:

     0   00 34 32 00   .42.   -- xid (any number)
     4   00 00 00 00   ....   -- mtype
     8   00 00 00 02   ....   -- rpcver (2)
    12   00 01 86 a3   ....   -- prog (nfs = 100003)
    16   00 00 00 02   ....   -- vers (2)
    20   00 00 00 00   ....   -- proc (NFSPROC_NULL = 0)
    24   ...

This should continue with two `opaque_auth` structures
(one for request, other for reply) defined as:

    struct opaque_auth {
        auth_flavor flavor;
        opaque body<400>;
    };

`flavor` can be AUTH_NULL = 0 for NFS "do nothing" call
(NFSPROC_NULL = 0). NFS also describes "mount service"
where AUTH_NULL is possible. Let's continue:

    24   00 00 00 00   ....   -- cred.flavor (AUTH_NULL)
    28   00 00 00 00   ....   -- cred.body length
    32   00 00 00 00   ....   -- verf.flavor (AUTH_NULL)
    36   00 00 00 00   ....   -- verf.body length

40 bytes in total for an empty request.


--[NFS v2]--

There is no NFS version 1, because it was closed alpha.

https://tools.ietf.org/html/rfc1094

