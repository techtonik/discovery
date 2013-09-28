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
# check dependencies and fetch them if neeeded
try:
  import httplib2
  import apiclient
except ImportError as exc:
  print('Dependencies are not importable. Bootstrapping locally.')
  speccy = {
    'httplib2': (
      'httplib2-0.8.zip',
      'https://httplib2.googlecode.com/files/httplib2-0.8.zip',
      'bb79080bc94d5e01f8ca3b79ba449a5b169c5e72 159827'),
    'apiclient': (
      'google-api-python-client-1.2.zip',
      'https://google-api-python-client.googlecode.com/files/google-api-python-client-1.2.zip',
      '4e82bbc87e17acf70606ba45b379ea6c5095dd63 97080')
  }
  if 'httplib2' not in exc.message:
    speccy.pop('httplib2')

  # [ ] create .locally if not exists
  # [ ] wgetsecure(.locally, speccy)
  
# ---[ /bootstrap ]---

# ---[ boilerplate from quickstart.py example ]---
# ---[ /boilerplate ]---


if __name__ == '__main__':
  # [ ] command line usage: drive.py upload <filename>
  pass
