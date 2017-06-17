This exposes two function in Python API for Far Manager:

  * `GetUserScreen` - switches current screen buffer to standard
    console that is hiding behind the panel. All printed output
    will directly go there.

  * `SetUserScreen` - switch current screen buffer to panels.

For low level API see `FCTL_SETUSERSCREEN` and
`FCTL_GETUSERSCREEN` descriptions at
https://api.farmanager.com/ru/service_functions/panelcontrol.html
