"""
High level Plugin class.

"""

__title__ = "04class"
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
plugin = None

class FarPlugin:
    title = __title__                          # should be set and non-empty
    author = __author__                        # should be set and non-empty
    title = __title__
    # first string from file comment
    description = __doc__.strip().splitlines()[0]

    # --- callbacks for obligatory Far plugin interface
    # first call made by Far at initialization
    def get_global_info(self, info):
        """ See GetGlobalInfoW """
        pass

    # second call made by Far at init
    def set_startup_info(self, farapi):
        self.api = farapi

    # third call made by Far to complete initialization
    def get_plugin_info(self, pluginfo):
        pluginfo["MenuString"] = self.title
        pluginfo["Guid"] = getuuid(self.title)

    # --- callbacks for optional Far plugin logic
    def open(self, info):
        print("[open] " + __file__)
        print("API:  {} {}".format(type(self.api), str(self.api)))
        print("info: {} {}".format(type(info), str(info)))


def GetGlobalInfoW(info):
    """ Called 1st by Far Manager, plugin needs to fill the `info` """
    global plugin
    info["Title"] = plugin.title             # should be set and non-empty
    info["Author"] = plugin.author           # should be set and non-empty
    info["Description"] = plugin.description # should be set
    info["Guid"] = getuuid(plugin.title)
    plugin.get_global_info(info)

def SetStartupInfoW(farapi):
    """ Called 2nd by Far Manager to pass pointer to API functions """
    global plugin
    plugin.set_startup_info(farapi)

def GetPluginInfoW(pluginfo):
    """ Called 3rd by Far Manager to add item into Plugin commands menu (F11) """
    global plugin
    plugin.get_plugin_info(pluginfo)

def OpenW(info):
    """ Called by Far Manager when plugin is invoked """
    global plugin
    plugin.open(info)


# --- specific plugin

plugin = FarPlugin()

