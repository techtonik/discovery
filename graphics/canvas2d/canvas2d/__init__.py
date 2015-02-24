"""
Canvas 2D is a set of API definitions for 2D drawing.

Its purpose is to:

 - document existing 2D drawing APIs
 - generate API compatibility tables by inspecting
   libraries
 - provide boilerplate for implementing new API
 - provide reference code for some drawing functions

"""

# get any available drawing canvas

# if no preference, try these:
# [ ] tkinter
# [ ] pyglet
# [ ] matplotlib
# [ ] pygame


# --- helper Table class

class Table(object):
    __table_api__ = '1.0'       # version of Table class API
    def __init__(self, *args):
        self._names = args
        self._rows = []
    def addrow(self, *args):
        self._rows.append(list(args))
    def update(self, idname, idvalue, name, value):
        idx = self._names.index(idname)
        tgtidx = self._names.index(name)
        for i,r in enumerate(self._rows):
            if r[idx] == idvalue:
                r[tgtidx] = value
    def __str__(self):
        text = ""
        for r in self._rows:
            text += str(r)
        return text

# --/ helper Table


# Python should really have a Table data type
BACKENDS = Table("name", "exists")
BACKENDS.addrow("tkinter", False)

def detect_backends():
    global BACKENDS
    import backtk
    if backtk.exists():
        BACKENDS.update("name", "tkinter", "exists", True)

detect_backends()

print(BACKENDS)
