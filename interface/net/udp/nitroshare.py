#!/usr/bin/env python
"""
Attempt to comunicate with Nitroshare.

 [x] listen nitroshare broadcasts and show who is available
   [x] listen for UDP packets on port 40816

"""

# --- communicating.. networking.. ---

import socket

IP4 = socket.AF_INET
UDP = socket.SOCK_DGRAM

class UDPSocketStream(object):
  """ Convert network socket endpoint to a readable stream object """
  def __init__(self, host='0.0.0.0', port=40816):
    # reading from socket blocks keyboard input, so CtrlC/CtrlBreak
    # may not work until read operation completes
    sock = socket.socket(IP4, UDP)
    # on socket level, allow multiple programs listen in the same address
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

def nitrolisten():
  import json
  s = UDPSocketStream()

  while True:
    data, remote = s.sock.recvfrom(1024)
    #print("Got packet!")
    #print data
    # msg = {u'uuid': u'{eb8d3a1e-c50f-459d-9be7-6a70b91ca6bd}', u'operating_system': u'linux', u'name': u'XONiTE', u'port': u'40818'}
    msg = json.loads(data)
    print("Got response from %s (%s) on %s:%s " % (msg[u'name'], msg[u'operating_system'].capitalize(), remote[0], msg[u'port']))

if __name__ == '__main__':
  nitrolisten()
