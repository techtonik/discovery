from __future__ import print_function
import timeit

print('--- performance of random data generator ---')

snippets = [
  ('urandom', '''\
import os

os.urandom(512-8)
'''),
   
  ('urandom def', '''\
import os
def osrandom(size):
  return os.urandom(size)

osrandom(512-8)
'''),

  ('randint', '''\
import struct, random

struct.pack((512-8)*'B', *[random.getrandbits(8) for _ in range(512-8)])
''')]

for name, snip in snippets:
  setup, body = snip.split('\n\n')
  print(name, end=' ')
  #print(setup, body)
  print(timeit.timeit(body, setup=setup, number=100000))

#print('urandom', timeit.timeit('os.urandom(512-8)', setup='import os', number=100000))
#print('urandom def', timeit.timeit('osrandom(512-8)', setup='import os\ndef osrandom(size): return os.urandom(size)', number=100000))
#print('randint', timeit.timeit("struct.pack((512-8)*'B', *[random.getrandbits(8) for _ in range(512-8)])", setup='import struct, random',  number=100000))
