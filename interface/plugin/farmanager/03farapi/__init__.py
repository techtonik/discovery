"""
Get access to low-level Far API functions.

 * https://api.farmanager.com/ru/exported_functions/
  
"""

__title__ = "03farapi"
__author__ = "anatoly techtonik <techtonik@gmail.com>"
__license__ = "Public Domain"


# --- utility functions ---

import hashlib

def getuuid(data):
    """Generate UUID from `data` string"""
    if type(data) != bytes:
        data = data.encode('utf-8')
    h = hashlib.sha256(data).hexdigest()[:32].upper()
    for i, pos in enumerate([8, 12, 16, 20]):
        h = h[:i+pos] + '-' + h[i+pos:]
    return h


# --- plugin interface

# passed by Far through SetStartupInfoW call
api = None

def GetGlobalInfoW(info):
    """ Called by Far Manager, plugin needs to fill the info """
    info["Title"] = __title__                          # should be set and non-empty
    info["Author"] = __author__                        # should be set and non-empty
    # first string from file comment
    desc = __doc__.strip().splitlines()[0]
    info["Description"] = desc                         # should be set
    info["Guid"] = getuuid(info["Title"])

def GetPluginInfoW(info):
    """ Called by Far Manager to add item into Plugin commands menu (F11) """
    info["MenuString"] = __title__
    info["Guid"] = getuuid(info["MenuString"])

def SetStartupInfoW(farapi):
    """ Called by Far Manager to pass pointer to API functions """
    global api
    api = farapi

def OpenW(info):
    global api
    """ Called by Far Manager when plugin is invoked """
    print("[open] " + __file__)
    print("Available API:\n - " + "\n - ".join(dir(api)))
