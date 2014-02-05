#!/usr/bin/env python
"""
Network server to receive GfxTables events based
on version 1 of this network tablet protocol.

https://github.com/rfc2822/GfxTablet/blob/master/doc/protocol.txt

Version 1
---------

GfxTablet app sends UDP packets to port 40118 of the destination host.

Packet structure, uses network byte order (big endian):

  9  bytes    "GfxTablet"
  2  bytes    version number
  1  byte     event:
                0 motion (hovering)
                1 control (finger, pen etc. touches surface)

  2  bytes    x (using full range: 0..65535)
  2  bytes    y (using full range: 0..65535)
  2  bytes    pressure (using full range 0..65535, 32768 == pressure 1.0f on Android device)

  when type == control event:
  1  byte     number of control, starting with 0
  1  byte     control status:
                0 control is off
                1 control is active

Comments:

 - use netcat to test server `nc -u 127.0.0.1 40118`

"""

__author__  = "anatoly techtonik <techtonik@gmail.com>"
__license__ = "MIT/Public Domain/CC0"
__version__ = "1.0.beta1"


# --- python helpers ---

def _none(msg):
  pass
def _printer(msg):
  print(msg)

# debugging helper, which can be turned turned off with
# echo = _none
echo = _printer


# --- communicating.. networking.. ---

import socket

IP4 = socket.AF_INET
UDP = socket.SOCK_DGRAM

def getmyips():
  """Return all IP addresses that belong to current machine

     [x] Windows returns only real LAN IP, no 127.x.x.x
     [ ] Linux, [ ] OS X  - unknown
  """
  return socket.gethostbyname_ex(socket.gethostname())[2]

class UDPSocketStream(object):
  """ Convert network socket endpoint to a readable stream object """
  def __init__(self, host='0.0.0.0', port=40118):
    # reading from socket blocks keyboard input, so CtrlC/CtrlBreak
    # may not work until read operation completes
    sock = socket.socket(IP4, UDP)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    self.sock = sock

  def read(self, size):
      return self.sock.recvfrom(size)[0]

  def close(self):
    try:
      self.sock.shutdown(socket.SHUT_RDWR)
    except:
      pass
    self.sock.close()

# --- /networking ---


# --- packet processing ---

import ctypes

CHAR = ctypes.c_ubyte
BYTE = ctypes.c_ubyte
WORD = ctypes.c_ushort  # two bytes
ENUM = ctypes.c_ubyte   # one byte, fixed set of values
INT  = ctypes.c_ushort  # two bytes, integer value

class Packet(ctypes.BigEndianStructure):
  _pack_ = 1
  _fields_ = [
    # 9  bytes   "GfxTablet"
    ('magic',   CHAR*9),   # string(9), [ ] ability to output .value
    # 2  bytes   version number
    ('version', WORD),     # word
                           # [ ] ability to output as hex
                           # [ ] to int
                           # [ ] to version tuple
    # 1  byte event:
    #         0 motion event (hovering)
    #         1 control event (finger, pen etc. touches surface)
    ('event',   ENUM),     # word
                           # [ ] to type string
                           # [ ] to some corresponding object
    ('x', INT),  # WORD, using full range: 0..65535
    ('y', INT),  # WORD, using full range: 0..65535
    ('pressure', INT),  # WORD, full range 0..65535,
                        # 32768 == pressure 1.0f on Android device

    # when event == control event,
    ('control', BYTE),    # number of control, starting with 0
    ('state', BYTE),     # control status - 0 off, 1 active
  ]

  def parse(self, bdata):
    fit = min(len(bdata), ctypes.sizeof(self))
    ctypes.memmove(ctypes.addressof(self), bdata, fit)

  def __len__(self):
    return ctypes.sizeof(self)


class Processor(object):
  def __init__(self):
    self.count = 0
    self.packet = Packet()

  def process(self, b):  # b is a binary string
    self.count += 1
    if not b.startswith('GfxTablet'):
      echo('#%3s  (discarded) invalid signature' % self.count)
      return
    # packet accepted
    msg1 = '#%3s  (got %s bytes)' % (self.count, len(b))
    #debug    echo(msg1)
    #debug    import hexdump; hexdump.hexdump(b)
    self.packet.parse(b)
    if self.packet.version != 1:
      echo('  warn: only version 1 of protocol is supported')
    msg2 = 'event:%s  x,y:%s,%s  pressure:%s' % (self.packet.event,
               self.packet.x, self.packet.y, self.packet.pressure)
    if len(b) == len(self.packet):
      state = 'active' if self.packet.state else 'inactive'
      msg2 += '  control:%s %s' % (self.packet.control, state)
    echo(msg1 + '  ' + msg2)
    return self.packet
    
# --- /parsing ---


# Get last IP from all available
ip = getmyips()[-1]

print('GfxTablet Server IP: %s' % ip)
s = UDPSocketStream()
p = Processor()

try:
  import autopy
except ImportError:
  print('..autopy is not installed, mouse control is disabled')

while True:
  res = p.process(s.read(1024))
  if autopy:
    # normalize screen coordinates
    width, height = autopy.screen.get_size()
    x, y = res.x*width//32768, res.y*height//32768
    #print x,y
    autopy.mouse.move(x, y)
    if res.event == 1 and res.state == 1:
      autopy.mouse.click()
