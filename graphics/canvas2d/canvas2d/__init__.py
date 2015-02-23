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

# Python should really have a Table data type
BACKENDS = {
  "tkinter": False,
}

def detect_backends():
    # [ ] make a copy
    detected = BACKENDS
    try:
        import Tkinter
        detected["tkinter"] = True
    except ImportError:
        pass
    return detected

print(detect_backends())
