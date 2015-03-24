
# --- helpers ---

import imp
def module_importable(name):
    try:
        imp.find_module(name)
        return True
    except ImportError:
        return False

# --- plugin interface ---

def exists():
    return module_importable('Tkinter')

def init():
    global Tkinter
    import Tkinter

# --- namespace for storing state ---

class CanvasNamespace(object):
    def __init__(self, width, height):
        self.mainwindow = Tkinter.Tk()
        self.canvas = Tkinter.Canvas(self.mainwindow, width=width, height=height)

# --- public API

def get_canvas(width, height):
    """create and return module Canvas element"""
    return CanvasNamespace(width, height)
