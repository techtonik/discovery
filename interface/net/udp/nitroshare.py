#!/usr/bin/env python
"""
NitroShare server discovery.

https://github.com/nitroshare/nitroshare-desktop/wiki/Broadcast-Protocol

 [x] listen nitroshare broadcasts and show who is available
   [x] listen for UDP packets on port 40816

"""

# --- communicating.. networking.. ---

import socket

IP4 = socket.AF_INET
UDP = socket.SOCK_DGRAM

class UDPSocketStream(object):
  """ Convert network socket endpoint to a readable stream object """
  host = None
  port = None

  def __init__(self, host='0.0.0.0', port=0):
    """
    By default, listen on all interfaces on random port.
    """
    # reading from socket blocks keyboard input, so CtrlC/CtrlBreak
    # may not work until read operation completes
    sock = socket.socket(IP4, UDP)
    # on socket level, allow multiple programs listen in the same address
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    self.sock = sock
    self.host, self.port = sock.getsockname()

  def read(self, size):
      return self.sock.recvfrom(size)[0]

  def close(self):
    try:
      self.sock.shutdown(socket.SHUT_RDWR)
    except:
      pass
    self.sock.close()

# --- /networking ---

# --- monitoring ---

import json
import collections
import time

# list of last 100 Peers
#   uuid, os, name, host, port, tls, time
peers = collections.deque(maxlen=100)

class Peer(object):
  def __init__(self, jsonmsg, host):
    self.uuid = jsonmsg[u'uuid']
    self.os   = jsonmsg[u'operating_system'].capitalize()
    self.name = jsonmsg[u'name']
    self.host = host
    self.port = jsonmsg[u'port']
    self.tls  = jsonmsg[u'uses_tls']
    self.time = time.time()

  def __str__(self):
    return "{0.name} ({0.os}) {0.host}:{0.port}".format(self)

# --- /monitoring ---
  

def nitrolisten():
  import json
  s = UDPSocketStream(port=40816)
  print("Listening for NitroShare on %s:%s" % (s.host, s.port))

  while True:
    data, remote = s.sock.recvfrom(1024)
    #print("Got packet!")
    #print data
    # msg = {u'uuid': u'{eb8d3a1e-c50f-459d-9be7-6a70b91ca6bd}', u'operating_system': u'linux', u'name': u'XONiTE', u'uses_tls': False, u'port': u'40818'}
    msg = json.loads(data)

    peer = Peer(msg, host=remote[0])
    print("Got response from {0}".format(peer))
    peers.append(peer)

if __name__ == '__main__':
  nitrolisten()
