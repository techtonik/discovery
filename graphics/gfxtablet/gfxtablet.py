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
  1  byte     type:
                0 motion event (hovering)
                1 control event (finger, pen etc. touches surface)

  2  bytes    x (using full range: 0..65535)
  2  bytes    y (using full range: 0..65535)
  2  bytes    pressure (using full range 0..65535, 32768 == pressure 1.0f on Android device)

  when type == control event:
  1  byte     number of control, starting with 0
  1  byte     control status:
                0 control is inactive
                1 control is active

Comments:

 - use netcat to test server `nc -u 127.0.0.1 40118`

"""

__author__  = "anatoly techtonik <techtonik@gmail.com>"
__license__ = "MIT/Public Domain/CC0"
__version__ = "1.0.alpha2"


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

class Processor(object):
  def __init__(self):
    self.count = 0

  def process(self, b):  # b is a binary string
    self.count += 1
    if not b.startswith('GfxTablet'):
      echo('#%3s  (discarded) invalid signature' % self.count)
      return
    echo('#%3s  (accepted) (%s bytes)' % (self.count, len(b)))
    
# --- /parsing ---


# Get last IP from all available
ip = getmyips()[-1]

print('GxfTablet Server IP: %s' % ip)
s = UDPSocketStream()
p = Processor()
while True:
  p.process(s.read(1024))
