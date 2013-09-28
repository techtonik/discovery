'''
Attempt to automate steps necessary for uploading stuff
to Google Drive. Based on steps listed on:
https://developers.google.com/drive/quickstart-python

1. Enable the Drive API
  1. Create API project
     https://code.google.com/apis/console/?pli=1
  2. Enable the Drive API in Services
  3. Open API Access tab and create an OAuth 2.0 client ID
  4. Set application name (e.g. "Drive Quickstart Sample")
  5. Client ID Settings section:
    1. Installed application
    2. Other
  5. From the API Access page, you'll need Client ID
     and Client Secret info.
  
Author: anatoly techtonik <techtonik@gmail.com>
License: Public Domain
'''

from config import CLIENT_ID, CLIENT_SECRET



# ---[ bootstrap section ]---
# check dependencies and fetch them if needed

# --[cut locally.py]--
# ---[ download utilities ]---

from hashlib import sha1
import os.path as osp
import urllib
import os

def hashsize(path):
  '''
  Generate SHA-1 hash + file size string for the given
  filename path. Used to check integrity of downloads.
  Resulting string is space separated 'hash size':

    >>> hashsize('locally.py')
    'fbb498a1d3a3a47c8c1ad5425deb46b635fac2eb 2006'
  '''
  size = osp.getsize(path)
  h = sha1()
  with open(path, 'rb') as source:
    while True:
      c = source.read(64*1024)  # read in 64k blocks
      if not c:
        break
      h.update(c)
  return '%s %s' % (h.hexdigest(), size)

class HashSizeCheckFailed(Exception):
  '''
  Exception to throw when downloaded file fails hash
  and size check.
  '''
  pass

def wgetsecure(targetdir, filespec, quiet=False):
  '''
  Using description in `filespec` list, download
  files from specified URL (if they don't exist)
  and check that their size and sha-1 hash matches.

  Files are downloaded into `targetdir`. `filespec`
  is list of tuples (filename, 'hash size', URL).

    filespec = [
     ('wget.py',
      '4eb39538d9e9f360643a0a0b17579f6940196fe4 12262',
      'https://bitbucket.org/techtonik/python-wget/raw/2.0/wget.py'),
    ]

  Raises HashSizeCheckFailed if hash/size check
  fails. Set quiet to false to skip printing
  progress messages.
  '''
  # [-] no rollback
  def check(filepath, shize, quiet):
    if not quiet:
      print('Checking hash/size for %s' % filepath)
    if hashsize(filepath) != shize:
      raise HashSizeCheckFailed(
                'Hash/Size mismatch\n  exp: %s\n  act: %s'
                % (shize, hashsize(filepath)))

  for f, shize, url in filespec:
    filepath = osp.join(targetdir, f)
    # [x] download file if not exists
    if osp.exists(filepath):
      if not quiet:
        print("Downloading " + f + " skipped (already downloaded).")
      # [x] do not remove file if it exists and check failed
      check(filepath, shize, quiet)
    else:
      if not quiet:
        print("Downloading %s into %s" % (f, targetdir))
      urllib.urlretrieve(url, filepath)
      try:
        check(filepath, shize, quiet)
      except HashSizeCheckFailed:
        # [x] remove file if it was downloaded and check failed
        os.remove(filepath)
        raise

# ---[ /download utils ]---
# --[/cut locally.py]--


try:
  import httplib2
  import apiclient
except ImportError as exc:
  # --- bootstrap .locally ---
  #
  # this creates .locally/ subdirectory and sets few global
  # variables for convenience:
  #
  #   ROOT  - absolute path to this dir
  #   LOOT  - absolute path to the .locally/ subdir, added to
  #           to sys.path, always ends with /

  import os
  import sys
  ROOT = os.path.abspath(os.path.dirname(__file__))
  LOOT = os.path.join(ROOT, '.locally/')

  # try to bootstrap from .locally/
  sys.path.insert(0, LOOT)

  try:
    import httplib2
    import apiclient
  except ImportError as exc:
    print('Dependencies are not importable.')
    print('Bootstrapping dependencies locally..')

    if not os.path.exists(LOOT):
      print('..creating subdir')
      os.makedirs(LOOT)

    # downloading files
    speccy = {
      'httplib2': (
        'httplib2-0.8.zip',
        'bb79080bc94d5e01f8ca3b79ba449a5b169c5e72 159827',
        'https://httplib2.googlecode.com/files/httplib2-0.8.zip'),
      'apiclient': (
        'google-api-python-client-1.2.zip',
        '4e82bbc87e17acf70606ba45b379ea6c5095dd63 97080',
        'https://google-api-python-client.googlecode.com/files/google-api-python-client-1.2.zip'),
    }
    if 'httplib2' not in exc.message:
      speccy.pop('httplib2')

    for spec in speccy.values():
      filename = spec[0]
      print(".[%s]" % filename)
      if os.path.exists(LOOT + filename):
        print("..already downloaded to " + filename)
        print("..checking")
      else:
        print("..downloading to " + filename)
      wgetsecure(LOOT, [spec], quiet=True)
     

  # [ ] create .locally if not exists
  # [ ] wgetsecure(.locally, speccy)
  
# ---[ /bootstrap ]---

# ---[ boilerplate from quickstart.py example ]---
# ---[ /boilerplate ]---


if __name__ == '__main__':
  # [ ] command line usage: drive.py upload <filename>
  pass
