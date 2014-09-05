"""

"""
__author__  = "anatoly techtonik <techtonik@gmail.com>"
__license__ = "MIT/Public Domain/CC0"
__version__ = "0.1.alpha1"

# --- hexdump 3.x ---

import binascii
import sys

PY3K = sys.version_info >= (3, 0)

def dehex(hextext):
  # remove spaces and convert
  if PY3K:
    result = bytes.fromhex(hextext)
  else:
    hextext = "".join(hextext.split())
    result = hextext.decode('hex')
  return result

def chunks(seq, size):
  '''Generator that cuts sequence (bytes, memoryview, etc.)
     into chunks of given size. If `seq` length is not multiply
     of `size`, the lengh of the last chunk returned will be
     less than requested.

     >>> list( chunks([1,2,3,4,5,6,7], 3) )
     [[1, 2, 3], [4, 5, 6], [7]]
  '''
  d, m = divmod(len(seq), size)
  for i in range(d):
    yield seq[i*size:(i+1)*size]
  if m:
    yield seq[d*size:]

def dump(binary, size=2):
  '''
  Convert `binary` bytes (Python 3) or str (Python 2) to
  hex string like '00 00 00 00 00 00 00 00 00 00 00'.
  `size` of chunks can be specified as second argument.
  '''
  hexstr = binascii.hexlify(binary)
  if PY3K:
    hexstr = hexstr.decode('ascii')
  return ' '.join(chunks(hexstr.upper(), size))

# --- /hexdump ---


# --- netsend.py ---

import socket

IP4 = socket.AF_INET
UDP = socket.SOCK_DGRAM

class udp(object):
  """
  UDP client for sending arbitrary data over network.
  Synchronous (blocking), but supports timeouts.
  """

  def __init__(self, sendto, port, data=None, timeout=60):
    """
    If data is not None, send it immediately. Timeout is
    in seconds.
    """
    self.sendto = sendto
    self.portto = port
    self.sock = socket.socket(IP4, UDP)
    self.sock.settimeout(timeout)
    # counters
    self.sent = 0
    self.totalsent = 0
    self.received = 0
    self.totalreceived = 0
    # if port=0, system chooses random one for sending
    self.sock.bind(('', 0))
    if data:
      self.send(data)

  def send(self, data):
      self.sent = self.sock.sendto(data, (self.sendto, self.portto))
      self.totalsent += self.sent
      return self.sent

  def read(self, size):
      data = self.sock.recv(size)
      self.received = len(data)
      self.totalreceived += self.received
      return data

  def close(self):
    try:
      self.sock.shutdown(socket.SHUT_RDWR)
    except:
      pass
    self.sock.close()

# --- /netsend.py ---

if __name__ == '__main__':
  call = """
       0   00 34 32 00   .42.   -- xid (any number)
       4   00 00 00 00   ....   -- mtype
       8   00 00 00 02   ....   -- rpcver (2)
      12   00 01 86 a3   ....   -- prog (nfs = 100003)
      16   00 00 00 02   ....   -- vers (2)
      20   00 00 00 00   ....   -- proc (NFSPROC_NULL = 0)
      24   00 00 00 00   ....   -- cred.flavor (AUTH_NULL)
      28   00 00 00 00   ....   -- cred.body length
      32   00 00 00 00   ....   -- verf.flavor (AUTH_NULL)
      36   00 00 00 00   ....   -- verf.body length
"""
  call = "".join([line.split(None, 1)[1][:13] for line in call.strip().splitlines()])
  bindata = dehex(call)

  print("CALL:  " + dump(bindata, size=8))
  client = udp('192.168.1.34', 111, data=bindata)
  print("REPLY: " + dump(client.read(100500), size=8))
  client.close()
