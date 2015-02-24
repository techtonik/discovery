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

def CanvasNamespace(object):
    def __init__(self, width, height):
        self.mainwindow = Tkinter.Tk()
        self.canvas = Tkinter.Canvas(self.mainwindow, width, height)

canvas = None   # initialized by get_canvas()

# --- public API

def get_canvas(width, height):
    """create and return module Canvas element"""
    global canvas
    if not canvas:
        canvas = CanvasNamespace(width, height)
    return canvas
