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
# [x] initialization sets columns names
# [x] method to add row
# [x] method to find and update cell using lookup values
# [x] can be printed as a string
# [x] supports iteration row by row
# [x] return row as OrderedDict for easy access

from collections import OrderedDict

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
    def __iter__(self):
        for r in self._rows:
            yield OrderedDict(zip(self._names, r))

# --/ helper Table


# Python should really have a Table data type
BACKENDS = Table("name", "exists", "module")
BACKENDS.addrow("tkinter", False, None)

def detect_backends():
    global BACKENDS
    import backtk
    if backtk.exists():
        BACKENDS.update("name", "tkinter", "exists", True)
        BACKENDS.update("name", "tkinter", "module", backtk)

canvas = None
detect_backends()
for backend in BACKENDS:
    if backend['exists']:
        canvas = backend['module'].get_canvas(320, 240)

