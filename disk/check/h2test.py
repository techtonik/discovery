"""
[ ] factor out test data generation code
[ ] scan size of existing test data 
[ ] handle OSError exception gracefully
[ ] speed up and test writing - very slow

[ ] random data doesn't match one produced by h2testw.exe
"""

# --- helpers ---
def endless_integers():
  l = 1
  while True:
    yield l
    l += 1

gennum = endless_integers()
# /-- helpers ---


from struct import pack, unpack
import random
import array

# write files (each max 1Gb) until run out of space
in1mb = 1024**2  # 1Mb
in1gb = 1024**3
sectsize = 512
secin1gb = in1gb / sectsize

for fileno in gennum:
  filename = "%s.h2w" % fileno
  f = open(filename, 'wb')
  # writing 1Gb files in 1Mb chunks
  try:
    for chunkno in range(1024):  # in 1Gb 1024*1Mb
      # offset is written at the start of each sector
      # it is also a seed for random data for this sector
      data = array.array('B')
      start = (fileno-1)*in1gb
      for offset in range(start+chunkno*in1mb, start+(chunkno+1)*in1mb, 512):
        # offset (4 words) first, random data (512-8 bytes) second
        random.seed(offset)
        binary = pack('<Q', offset)
        data.extend(unpack('8B', binary))
        data.extend(pack((512-8)*'B', *[random.getrandbits(8)
                                          for _ in range(512-8)]))
      print('---', 1+(offset//in1mb), '---')
      f.write(data.tostring())
  finally:
    f.close()      

"""
--- 9819 ---
Traceback (most recent call last):
  File "C:\Users\anatoli\Downloads\H2TESTW\h2testw_1.4\h2testw.py", line 46, in <module>
    f.write(data.tostring())
OSError: [Errno 28] No space left on device
"""
