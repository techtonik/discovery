try:
  import Tkinter
except ImportError:
  Tkinter = False

# --- plugin interface ---

def exists():
    if not Tkinter:
        return False
    return True

# --- namespace for storing state ---

class CanvasNamespace(object):
    def __init__(self, width, height):
        self.mainwindow = Tkinter.Tk()
        self.canvas = Tkinter.Canvas(self.mainwindow, width=width, height=height)

# --- public API

def get_canvas(width, height):
    """create and return module Canvas element"""
    return CanvasNamespace(width, height)
