https://github.com/techtonik/discovery/tree/master/interface/plugin/farmanager

Note: Examples in 00xxx/ dirs are for previous versions of pygin API -
      pygin_89f1868_090517.7z and below. They don't work with pygin_140517_6b26d5f.7z
      and later.

1. Download `pygin*.7z` from https://forum.farmanager.com/viewtopic.php?f=8&t=9998  
2. Unpack `pygin.dll` into Adapters/ subdir of your Far directory (%FARHOME%)
3. Create your plugin in %FARHOME%/Plugins as Python package (dir with `__init__.py`)
4. Restart, press F11 to see your plugin in the list, F3 to see more info
5. If something goes wrong, check %TMP%/pygin.log for errors and output


Here is an example plugin. Feel free to copy and adapt.
```python
"""
Class-based Far API.

"""

__title__ = "10class"
__author__ = "anatoly techtonik <techtonik@gmail.com>"
__license__ = "Public Domain"


# --- utility functions ---

import hashlib
import uuid

def getuuid(data):
    """Generate UUID from `data` string"""
    if type(data) != bytes:
        data = data.encode('utf-8')
    h = hashlib.sha256(data).hexdigest()[:32].upper()
    #for i, pos in enumerate([8, 12, 16, 20]):
    #    h = h[:i+pos] + '-' + h[i+pos:]
    return uuid.UUID(h)


# --- plugin interface

import pygin

# Far looks for FarPluginClass to initalize plugin

class FarPluginClass:
    Title = __title__                          # should be set and non-empty
    Author = __author__                        # should be set and non-empty
    # first string from file comment
    Description = __doc__.strip().splitlines()[0]
    Guid = getuuid(__title__)

    # --- callbacks for obligatory Far plugin interface
    def __init__(self, farapi):
        """ Called by Far at plugin initialization to pass its API """
        self.farapi = farapi

    def GetPluginInfoW(self):
        """ Called by Far Manager to query plugin capabilities and add it to
            specific parts of the interface, such as plugin menu, editor, disk
            menu, configuration.
        """
        info = self.farapi.PluginInfo()
        info.PluginMenuItems = [ (self.Title, getuuid(self.Title)) ]
        return info

    # --- callbacks for optional Far plugin logic
    def OpenW(self, info):
        """ Called by Far Manager when plugin is invoked """
        self.farapi.GetUserScreen()     # make console buffer active
        print("[open] " + __file__)
        print("API:  {}".format(self.farapi))
        print("info: {}".format(info))
        self.farapi.SetUserScreen()     # make panel buffer active
```


 * [Far API reference](https://api.farmanager.com/ru/exported_functions/)
