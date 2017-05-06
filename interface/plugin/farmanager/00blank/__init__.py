"""
Basic Far Manager plugin.

Copy dir to %FARHOME%/Plugins, restart Far, press F11, select "blank00", F3.

Everything should be self-explanative, except GUID fields. Those are basically
identifiers for plugin (name is not enough for some reason) and menu items
(menu string is not enough or some reason). Plugin works without them, but
there is some FUD.

 * [ ] dispell GUID FUD, explain how they are actually used

You need to change all GUIDs for your every new plugin, so be careful when
copypasting.


Low-level Far Manager API is here:

 * https://api.farmanager.com/en/exported_functions/getglobalinfow.html
  
"""

def GetGlobalInfoW(info):
    """ Called by Far Manager, plugin needs to fill the info """
    info["Title"] = "____"                             # should be set and non-empty
    info["Author"] = "_"                               # should be set and non-empty
    info["Description"] = "Simple Python plugin"       # should be set
    info["Guid"] = "3117D11E-B9D8-4A9B-88C7-2D2983802C50"  # optional, but...

def GetPluginInfoW(info):
    info["MenuString"] = "00blank"
    info["Guid"] = "4117257B-E011-4B5A-B5DC-732581BDF3B4"

def OpenW(info):
    print(__file__)
    print("GUIDs are Evil! Compute them based on module name/package.\n")
