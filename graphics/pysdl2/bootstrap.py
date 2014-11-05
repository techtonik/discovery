#!/usr/bin/env python
#
# Bootstrap PySDL2 by fetching SDL2 binaries (Windows)
# and the PySDL2 library itself.
#
# Use `locally` bootstrap code to securely fetch SDL2
# binaries using known hash/size combination, unpack
# them locally and optionaly run PySDL2 tests on them.

# This stuff is placed into public domain by
#    anatoly techtonik <techtonik@gmail.com>

# --- bootstrap .locally --
#
# this creates .locally/ subdirectory in the script's dir
# and sets a few global variables for convenience:
#
#   ROOT  - absolute path to source code checkout dir
#   LOOT  - absolute path to the .locally/ subdir
#
# this provides some helpers:
#
#   localdir(name)   - returns absolute path to the new `name`
#                      dir created .locally
#   extract_zip(zippath, subdir, target)
#                    - extracts subdir from the zip file
#   getsecure(names)
#                    - download files and check hash/size

FILESPEC = [
  dict(
    name='pysdl2',
    filename='PySDL2-0.9.3.zip',
    hashsize='030f2351d1da387f878e14c8a86e08571d7baf5b 1085634',
    url='https://bitbucket.org/marcusva/py-sdl2/downloads/PySDL2-0.9.3.zip',
    checkpath='PySDL2'
  ),
  dict(
    name='sdl2-win32',
    filename='SDL2-2.0.3-win32-x86.zip',
    hashsize='806a7f4890f598a7f2047d1fd36c3af13963e56f 396930',
    url='http://www.libsdl.org/release/SDL2-2.0.3-win32-x86.zip',
    checkpath='PySDL2/SDL2.dll'
  ),
  dict(
    name='sdl2-win64',
    filename='SDL2-2.0.3-win32-x64.zip',
    hashsize='b5c7dcb5d13c480ff5133691ffd96e28e8cb75fa 462897',
    url='http://www.libsdl.org/release/SDL2-2.0.3-win32-x64.zip',
    checkpath='PySDL2/SDL2.dll'
  ),
]

# convenient access to table cells as lookup('pysdl2', 'path')
def lookup(name, field, table=FILESPEC):
  """return `field` value for the row with given `name`"""
  for row in table:
    if row['name'] == name:
      return row[field]


import os
import sys
try:
  from urllib import urlretrieve  # Python 2
except ImportError:
  from urllib.request import urlretrieve

# 1. create .locally subdir

ROOT = os.path.abspath(os.path.dirname(__file__))
LOOT = os.path.join(ROOT, '.locally/')
if not os.path.exists(LOOT):
  os.mkdir(LOOT)

def localdir(name):
  '''create dir in LOOT if needed, return path with ending '/' '''
  nupath = LOOT + '/' + name + '/'
  if not os.path.exists(nupath):
    os.makedirs(nupath)
  return nupath

# 2. helpers for secure download with hash and size check

from hashlib import sha1
from os.path import exists, getsize, join

def hashsize(path):
  # calculate SHA-1 hash + file size string 
  size = getsize(path)
  h = sha1()
  with open(path, 'rb') as source:
    h.update(source.read())
  return '%s %s' % (h.hexdigest(), size)

class HashSizeCheckFailed(Exception):
  '''Throw when downloaded file fails hash and size check.'''
  pass

def getsecure(names, targetdir=LOOT):
  def check(filepath, shize):
    if hashsize(filepath) != shize:
      raise HashSizeCheckFailed(
                'Hash/Size mismatch for %s\n  exp: %s\n  act: %s'
                % (filepath, shize, hashsize(filepath)))

  for name in names:
    f = lookup(name, 'filename')
    shize = lookup(name, 'hashsize')
    url = lookup(name, 'url')
    filepath = join(targetdir, f)
    downloaded = False
    if exists(filepath):
      print("Downloading " + f + " skipped (already downloaded)")
    else:
      print("Downloading %s into %s" % (f, targetdir))
      urlretrieve(url, filepath)
      downloaded = True

    if not shize:
      print("Hash/size is not set, check skipped..")
    else:
      try:
        check(filepath, shize)
      except HashSizeCheckFailed:
        if downloaded:
          os.remove(filepath)
        raise

# --- /bootstrap


# 3. downloading PySDL2 and SDL2 binary

# [x] Windows 32/64
# [ ] Linux / Mac OS

files = ['pysdl2']
is_32bits = not (sys.maxsize > 2**32)
if is_32bits:
  files.append('sdl2-win32')
else:
  files.append('sdl2-win64')


print('Downloading PySDL2 and binary for SDL2 lib..')

getsecure(files)

def extract_zip(zippath, subdir, target):
  '''extract entries from `subdir` of `zipfile` into `target`/ directory'''
  from os.path import join, exists, dirname
  import shutil
  import zipfile
  zf = zipfile.ZipFile(zippath)
  
  dirs = set()  # cache to speed up dir creation

  for entry in zf.namelist():
    if subdir:
      if not entry.startswith(subdir + '/'):
        continue
      else:
        outfilename = join(target, entry.replace(subdir + '/', ''))
    else:
      outfilename = join(target, entry)

    # create directory for directory entry
    if outfilename.endswith('/'):
      if not exists(outfilename):
        os.makedirs(outfilename)
      continue
    # some .zip files don't have directory entries
    outdir = dirname(outfilename)
    if (outdir not in dirs) and not exists(outdir):
        os.makedirs(outdir)
        dirs.add(outdir)

    print(outfilename)

    outfile = open(outfilename, "wb")
    infile = zf.open(entry)
    shutil.copyfileobj(infile, outfile)
    outfile.close()
    infile.close()
  zf.close()

# unpack everything into PySDL2 subdir
SDL2DIR = localdir('PySDL2')
# and add it to sys.path to make importable
sys.path.insert(0, SDL2DIR)
# PYTHONPATH is needed for test subprocesses
os.environ['PYTHONPATH'] = SDL2DIR


if is_32bits:
  zipname = lookup('sdl2-win32', 'filename')
else:
  zipname = lookup('sdl2-win64', 'filename')
zippath = LOOT + zipname
if os.path.exists(SDL2DIR + 'README-SDL.txt'):
  print("..SDL2 already extracted.")
else:
  print("..extracting SDL2..")
  extract_zip(zippath, '', SDL2DIR)

zipname = lookup('pysdl2', 'filename')
zippath = LOOT + zipname
subdir = zipname.rsplit('.', 1)[0]
if os.path.exists(SDL2DIR + 'README.txt'):
  print("..PySDL2 already extracted.")
else:
  print("..extracting PySDL2..")
  extract_zip(zippath, subdir, SDL2DIR)

print("..done.")


# 4. import PySDL2

# specify location for SDL2 binaries
print("Setting PYSDL2_DLL_PATH to %s" % SDL2DIR)
os.environ["PYSDL2_DLL_PATH"] = SDL2DIR

# getting versions
import sdl2
import ctypes
pysdl2_version = sdl2.__version__
sdl2_version = sdl2.SDL_version()
sdl2.SDL_GetVersion(ctypes.byref(sdl2_version))

print("Imported SDL2 %s with SDL %s.%s.%s" % (sdl2.__version__,
  sdl2_version.major, sdl2_version.minor, sdl2_version.patch))
print("Bootstrap complete.")


# 5. run tests if executed standalone
if __name__ == '__main__':
  print("Press Enter to run tests for PySDL2..")
  try:
    raw_input()  # Python 2
  except NameError:
    input()
  
  print("Running tests for PySDL2..")

  # launch application code
  import sdl2.test
  sdl2.test.util.runtests.run()

  print("Done.")
