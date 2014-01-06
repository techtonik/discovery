#!/usr/bin/env python
"""
Network server to receive GfxTables events based
on version 1 of this network tablet protocol.

https://github.com/rfc2822/GfxTablet/blob/master/doc/protocol.txt

Public domain work by
anatoly techtonik <techtonik@gmail.com>
"""

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
      return self.sock.recvfrom(size)

  def close(self):
    try:
      self.sock.shutdown(socket.SHUT_RDWR)
    except:
      pass
    self.sock.close()

# Get last IP from all available
ip = getmyips()[-1]

print('GxfTablet Server IP: %s' % ip)
s = UDPSocketStream()
while True:
  print(s.read(1024))
