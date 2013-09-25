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

Client_ID = '000000000000.apps.googleusercontent.com'
Client_Secret = 'XXXxxx0000-X-XXXXXX_XXxx'
