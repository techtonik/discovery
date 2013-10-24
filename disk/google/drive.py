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
  6. From the API Access page get Client ID and
     Client Secret
  
Author: anatoly techtonik <techtonik@gmail.com>
License: Public Domain
'''
from __future__ import print_function

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

# extract_zip is patched version
#
# * improved comments
# * inserted prints
# * fix4arhives without entries for dirs

def extract_zip(zippath, subdir, target):
  '''
  Extract entries from `subdir` of `zipfile` into
  `target`/ directory.

  [ ] check about archives without dir entries

  [ ] security check (overwrite file in parent dir)
  '''

  from os.path import join, exists
  import shutil
  import zipfile
  zf = zipfile.ZipFile(zippath)

  for entry in zf.namelist():
    if subdir:
      if not entry.startswith(subdir + '/'):
        continue
      else:
        outfilename = join(target, entry.replace(subdir + '/', ''))
    else:
      outfilename = join(target, entry)

    if outfilename.endswith('/'):  # directory
      continue
    else:
      filedir = os.path.dirname(outfilename)
      if filedir and not exists(filedir):
        os.makedirs(filedir)
    outfile = open(outfilename, "wb")
    infile = zf.open(entry)
    shutil.copyfileobj(infile, outfile)
    outfile.close()
    infile.close()
  zf.close()

# --[/cut locally.py]--


try:
  import httplib2
  import apiclient
except ImportError as exc:
  print('---[Initialize]---')
  # --- bootstrap .locally ---
  #
  # this creates .locally/ subdirectory and sets few global
  # variables for convenience:
  #
  #   ROOT  - absolute path to this dir, ends with /
  #   LOOT  - absolute path to the .locally/ subdir, added to
  #           to sys.path, always ends with /

  import os
  import sys
  ROOT = os.path.abspath(os.path.dirname(__file__)) + '/'
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
      filepath = LOOT + filename
      print(".[%s]" % filename)
      if os.path.exists(filepath):
        print("..already downloaded to " + filepath)
        print("..checking")
      else:
        print("..downloading to " + filepath)
      wgetsecure(LOOT, [spec], quiet=True)

      # decompressing
      #  for these dependencies unpacked dir
      #  is equal to .zip name without extension
      checkdir = spec[0].rsplit('.', 1)[0]
      if os.path.exists(LOOT + checkdir):
        print('..not decompressing (checkdir exists)')
      else:
        print('..decompressing')
        extract_zip(filepath, '', LOOT)
      
    # patching sys.path
    #  for httplib2 dire strip .zip name
    dirname = speccy['httplib2'][0].rsplit('.', 1)[0]
    dirname = LOOT + dirname + '/python' + sys.version[0]
    sys.path.insert(0, dirname)
    #  for apiclient
    dirname = speccy['apiclient'][0].rsplit('.', 1)[0]
    dirname = LOOT + dirname
    sys.path.insert(0, dirname)

    import httplib2
    import apiclient

    print('---[Start]---')

# ---[ /bootstrap ]---


# ---[ boilerplate from quickstart.py example ]---
import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

# https://developers.google.com/drive/scopes - all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

if __name__ == '__main__':
  # [x] command line usage: drive.py upload <filename>
  if len(sys.argv[1:]) < 2 or sys.argv[1] != 'upload':
    sys.exit('Usage: drive.py upload <filename>')

  FILENAME = sys.argv[2]

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print('You need to get credentials from the following link:')
print(authorize_url)
print('Would you like to open browser automatically? [Yn]', end='')
answer = raw_input()
if len(answer.strip()) == 0 or answer.strip().lower() == 'y':
  import webbrowser
  webbrowser.open(authorize_url, new=2)

code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

# Insert a file
media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)
body = {
  'title': osp.basename(FILENAME),
}

file = drive_service.files().insert(body=body, media_body=media_body).execute()
pprint.pprint(file)

# ---[ /boilerplate ]---


