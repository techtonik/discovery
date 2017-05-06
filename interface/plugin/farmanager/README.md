https://gist.github.com/techtonik/9bfd6b3acac305ee64f2f4ec9ffffdfe

1. Download `pygin*.7z` from https://forum.farmanager.com/viewtopic.php?f=8&t=9998  
   (I tested with latest pygin_c080105_040517.7z)
2. Unpack `pygin.dll` into Adapters/ subdir of your Far directory (%FARHOME%)
3. Create your plugin in %FARHOME%/Plugins as Python package (dir with `__init__.py`)
4. Restart, press F11 to see your plugin in the list, F3 to see more info
5. If something goes wrong, check %TMP%/pygin.log for errors and output


Here is an example plugin. Feel free to copy and adapt.
```python
__title__ = "02fields"
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

def OpenW(info):
    """ Called by Far Manager when plugin is invoked  """
    print("[open] " + __file__)
```

For Far API refence, see
https://api.farmanager.com/ru/exported_functions/getglobalinfow.html