"""
Need to change all GUIDs for your every new plugin, is daunting, so let's
generate them from strings that are unique for plugins.


Low-level Far Manager API is here:

 * https://api.farmanager.com/en/exported_functions/getglobalinfow.html
  
"""

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

def GetGlobalInfoW(info):
    """ Called by Far Manager, plugin needs to fill the info """
    info["Title"] = "____"                             # should be set and non-empty
    info["Author"] = "_"                               # should be set and non-empty
    info["Description"] = "Simple Python plugin"       # should be set
    info["Guid"] = getuuid(info["Title"])

def GetPluginInfoW(info):
    info["MenuString"] = "01autoguid"
    info["Guid"] = getuuid(info["MenuString"])

def OpenW(info):
    print("[open] " + __file__)
