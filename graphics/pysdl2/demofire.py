#!/usr/bin/env python
"""
This is a reimplementation of old-school fire
algorithm. The algorithm:

  1. bottom line is randomly assigned colors
  2. other pixels are recalculated from left to
     right bottom to top
  3. pixel value is an average of four 
     surrounding ones

The original idea came from this post:

http://stackoverflow.com/questions/1918677/what-kind-of-cool-graphics-algorithms-can-i-implement

The code is placed into public domain
by anatoly techtonik <techtonik@gmail.com>
"""

__version__ = "1.6"

try:
  import sdl2
except ImportError:
  # securely download PySDL2 (Windows only for now)
  import bootstrap
  import sdl2

# window dimensions
WIDTH, HEIGHT  = 500, 100

print("---------------------------[ demofire %s ]---" % __version__)

# ---
# [x] create window
#
# [x] create game loop
#   [x] output  - draw world
#   [x] input
#   [x] process - update world
# ---

# ---
# [x] max FPS mode with measuring
# [ ] fixed FPS mode (25)
#   ---
#   [ ] measure CPU load for both
#   [ ] output results after window closed
#     [ ] optional mode with rendering on screen
# /--


# ------------------------- helpers ---

import time

class Timer(object):
  def __init__(self, seconds):
    self.seconds = seconds
    self.restart()

  def restart(self):
    self.end = time.time() + self.seconds

  @property
  def expired(self):
    return (time.time() > self.end)

class FPS(object):
  def __init__(self):
    self.counter = 0
    self.timer = Timer(1)
  def process(self):
    self.counter += 1
    if self.timer.expired:
      print("FPS: %s" % self.counter)
      self.counter = 0
      self.timer.restart()

# ---------------------------- init ---

import sdl2.ext as lib

lib.init()

window = lib.Window('HellFire', size=(WIDTH, HEIGHT))
window.show()

# renderer knows how to draw in a window, it provides
# universal interface to update window contents regardless
# of window type (GDI, OpenGL, ...)
renderer = lib.Renderer(window)


# ------- graphics helper functions ---

def vecsum(la, lb):
   """ (1,4,2) + (2,-1,1) == (3,3,3) """
   return tuple(a + b for a, b in zip(la, lb))

def vecop(la, lb, function):
   return tuple(function(a, b) for a, b in zip(la, lb))

def vecintlerp(l1, l2, pos):
   """ linear approximation for a vector of ints """
   return tuple( int(round(a1+(a2-a1)*pos)) for a1, a2 in zip(l1, l2))


def gradient(colors, n=256, wrapin=lib.Color):
   """generate gradient palette with `n` colors using
      key points from `colors` set as  (R,G,B) values
      (the process is known as interpolation). return
      list of sdl.ext.Color
   """
   if len(colors) == 1:           # o  is the same as  o--o
     colors.append(colors[0])
                                  # o--o---o--o
   steps = len(colors)-1          # no. of steps (spans) (3)
   addno = n-len(colors)          # no. of colors to fill
   spans = [(addno // steps)]*steps   # colors per span
                                  #  -- -- -- -   (3)+1
   rem = addno % steps

   if rem:
     spc = float(steps) / rem       # spans per remaining colors
     # distribute remaining colors
     for i in range(rem):
        # calculate the closest span for rem.color number i+1
        no = i+1                    # in math count starts with 1
        spanno = int(no * spc)
        spans[spanno-1] += 1        # in python count starts with 0

   palette = []
   # (10/3)  o--o---o--o [2,3,2]
   # (10/2)  o---o----o  [3,4]    or  (9/2)   o---o---o  [3,3]
   for i, rng in enumerate(spans):
      fr = colors[i]                # first color
      to = colors[i+1]              # second color
      palette.append(fr)

      for x in range(rng):       # 0,1
        xn = x+1                 # 1,2  - missing colors
        pos = float(xn)/(rng+1)  # 1/3, 2/3  - position on a line

        palette.append(vecintlerp(fr, to, pos))
        #print ".. " + str(veclerp(fr, to, pos))

   palette.append(colors[-1])
   if not wrapin:
     return palette
   else:
     return [wrapin(*pal) for pal in palette]

#print gradient([(9, 0, 0), (0, 0, 0), (18, 0, 0)], n=9)


# -------------------- define world ---
#
# world of scenes
#
class CyclicWorld(object):
  """world of scenes.

     window is also part of the world, because it has
     title that should be updated when scene changes"""

  def __init__(self, items, window):
    """every item is a scene"""
    if not items:
      raise ValueError("At least one element is required")
    self.items = items
    self.index = 0
    self.window = window
    self.fps = FPS()
    self.cycle(0)       # call refresh for the first scene

  def cycle(self, count=1):
    """`count` is any amount and can be negative"""
    self.index += count
    if self.index < 0 or self.index > len(self.items)-1:
      # modulo is a good operator for cycling in bounds
      self.index = self.index % len(self.items)
    self.scene = self.items[self.index]

    self.window.title = self.scene.title

    self.scene.switch()

  def process(self):
    self.scene.draw()
    self.fps.process()


# ------------------- define scenes ---

# every scene is an algorithm that produces some effect

class Scene(object):
  """scene knows about renderer and draws itself, it
     doesn't know anything about window (except size)"""

  width = WIDTH
  height = HEIGHT

  def __init__(self, renderer, title=None):
    """
    - renderer:  is a SDL2 renderer used for drawing
    - title:     scene / algoritm name. if not set, the
                 value is the 1st line of class docstring
                 or a class name
    """
    self.renderer = renderer
    if title:
      self.title = title
    elif self.__doc__:
      self.title = self.__doc__.splitlines()[0]
    else:
      self.title = self.__class__.__name__

  def draw(self):
    """called from main loop to draw frame"""
    pass

  def switch(self):
    """method called on scene switch"""
    pass


class PixelScene(Scene):
  """[A Pixel from Hell]"""
  def draw(self):
    renderer.draw_point([10,10], lib.Color(255,255,255))
    renderer.present()

  def switch(self):
    renderer.clear()

from random import randint
class PixelLine(Scene):
  def __init__(self, renderer, title=None):
    Scene.__init__(self, renderer, title)
    self.px = 10
    self.py = 10
    self.color = lib.Color(255,255,255)

  def draw(self):
    # draw
    renderer.draw_point([self.px, self.py], self.color)
    renderer.present()
    # process
    self.px += 1
    if self.px > WIDTH-10:
      self.px = 10
      self.py +=1
      self.color = lib.Color(randint(0,255),randint(0,255),randint(0,255))
      if self.py > HEIGHT-10:
        self.py = 10

class LineLine(Scene):
  def __init__(self, renderer, title=None):
    Scene.__init__(self, renderer, title)
    self.px = 10
    self.py = 10
    self.color = lib.Color(255,255,255)

  def draw(self):
    # draw
    renderer.draw_line([10, self.py, WIDTH-10, self.py], self.color)
    renderer.present()
    # process
    self.py += 1
    self.color = lib.Color(randint(0,255),randint(0,255),randint(0,255))
    if self.py > HEIGHT-10:
      self.py = 10

class Gradient(Scene):
  """[Gradient]: one line at a time"""
  def __init__(self, renderer, title=None):
    Scene.__init__(self, renderer, title)
    self.px = 10
    self.py = 10
    # make 256 colors pallette of reds
    self.palette = [lib.Color(x,0,0) for x in range(256)]
    self.coloridx = 0

  def draw(self):
    # draw
    renderer.draw_line([10, self.py, WIDTH-10, self.py], 
                       self.palette[self.coloridx])
    renderer.present()
    # process
    self.py += 1    
    if self.py > HEIGHT-10:
      self.py = 10
    # choose color based on current line number
    span = HEIGHT-10-10                # total number of drawn lines
    lidx = float(self.py-10) / span    # line position in span as percentage
    self.coloridx = int(255 * lidx)  # number in 256 color palette


class SingleStepGradient(Scene):
  """[Single Step Gradient]: all lines at once"""
  def __init__(self, renderer, title=None):
    Scene.__init__(self, renderer, title)
    self.px = 10
    self.py = 10
    self.palette = gradient( [(255,255,0), (170,0,0), (0,0,0)], n=256)
    self.coloridx = 0

  def draw(self):
    span = HEIGHT-10-10                # total number of drawn lines
    for y in range(10, HEIGHT-10+1):
      # choose color based on current line number
      lidx = float(y-10) / span    # line position in span as percentage
      coloridx = int(255 * lidx)   # number in 256 color palette
      renderer.draw_line([10, y, WIDTH-10, y],
                         self.palette[255-coloridx])
    renderer.present()


class PalRotate(SingleStepGradient):
  """[Rotate Pallette]"""
  def __init__(self, renderer, title=None):
    SingleStepGradient.__init__(self, renderer, title)
    self.palette = gradient( [(255,255,0), (170,0,0), (0,0,0)], n=256)

  def draw(self):
    shifted = self.palette.pop()
    self.palette.insert(0, shifted)
    SingleStepGradient.draw(self)


from random import randint
class PixelPlane(Scene):
  """[Pixel Noize]"""
  def __init__(self, renderer, title=None):
    Scene.__init__(self, renderer, title)
    self.py = 10   # start positions
    self.px = 10   # (never changes for this algorithm)
    self.palette = gradient( [(255,255,0), (170,0,0), (0,0,0)], n=256)

  def draw(self):
    # draw
    for x in range(10, WIDTH-self.px):
      renderer.draw_point([x, self.py], self.palette[randint(0,255)])
    renderer.present()

    # process
    self.py += 1    
    if self.py > HEIGHT-10:
      self.py = 10

  def switch(self):
    renderer.clear()

import copy
class FirePlane(PixelPlane):
  """[Fire Plane]: listed pixels, line per frame"""
  def __init__(self, renderer, title=None):
    PixelPlane.__init__(self, renderer, title)
    self.spanx = WIDTH-10-10
    self.spany = HEIGHT-10-10          # total number of lines to draw
    self.bottomline = HEIGHT-10-1
    self.py = self.bottomline
    # line based pixel buffer
    self.lines = [list()]*self.spany        # total lines
    for y in range(self.spany):
      self.lines[y] = [255]*self.spanx     # pixels in line

  def draw(self):
    # draw
    y = self.py-10
    self.recalculate(y)
    self.render_line(y)
    renderer.present()
    
    # process bottom to top
    self.py -= 1
    if self.py < 10:
      self.py = self.bottomline

  def recalculate(self, y):
    if y+10 == self.bottomline:
      # line with noize
      for x in range(self.spanx):
        self.lines[y][x] = randint(0,255)
    else:
      # line with fire
      for x,c in enumerate(self.lines[y]):  # color
        l = self.lines[y+1][max(x-1, 0)]    # bottom left
        b = c                               # self
        r = self.lines[y+1][min(x+1, self.spanx-1)] # bottom right
        self.lines[y][x] = (l+b+r) // 3

  def render_line(self, y):
    for x, colorno in enumerate(self.lines[y]):
      renderer.draw_point([x+10, y+10], self.palette[colorno])

# [ ] HellFire
  # line per frame algorithm
  # start scan from top to bottom
  # for every pixel from right to left, the color is
  #   (left + right + bottom) // 4
  # special cases: 
  #   bottom line, pixels are generated randomly


def linesin(line, piece, space):
  """ given a line size, piece and space size
      return number of pieces that will fit it and 
      0-based starting position as a tuple"""

  # [ ] test edge case - no pieces are fit
  pieces, rem = divmod(line+space, piece+space)
  if pieces == 0:
    return (0, 0)
  if rem == 0:
    # pieces match line exacly without left and
    # right borders, such as 10s10s10 == 32
    # linesin(32, 10, 1) == (3, 0)
    return pieces, rem
  else:
    return pieces, rem//2

class GridBox(Scene):
  def __init__(self, renderer, title=None):
    Scene.__init__(self, renderer, title)
    self.cubes = 0                 # cube counter
    self.space = 3
    # build a potential grid of cubes 10x10 with 1 space
    self.rows, self.rowoffs = linesin(self.width, 10, self.space)   # cells, startpx
    self.cols, self.coloffs = linesin(self.height, 10, self.space)  #
    self.max = self.rows*self.cols

    self.palette = [lib.Color(0,220,0), lib.Color(0,0,0)]
    self.colidx = 0
    self.color = self.palette[self.colidx]

  def draw(self):
    for i in range(self.cubes):
      col, row = divmod(i, self.cols)
      x = self.rowoffs+col*(10+self.space)
      y = self.coloffs+row*(10+self.space)
      renderer.fill([x,y,10,10], self.color)

    renderer.present()

    # [ ] recalculate in a separate on-demand method
    self.cubes += 1
    if self.cubes > self.max:
      self.cubes = 0
      self.colidx += 1
      if self.colidx == len(self.palette):
        self.colidx = 0
      print self.colidx
      self.color = self.palette[self.colidx]

  def switch(self):
    renderer.clear()

# ---------------- initialize world ---

# generate some empty scenes
names = ['Yo! Press Right to continue...']
names.extend(['Hello, World', 'of HellFire..'])
scenes = [Scene(renderer, title=name) for name in names]
# add first scene with *real* content
scenes.append(PixelScene(renderer))
# add scene that draws lines
scenes.append(PixelLine(renderer, title='[Lines of Pixel]'))
# add scene that draws lines by lines
scenes.append(LineLine(renderer, title='[Lines by Line]'))
# draw gradient using lines
scenes.append(Gradient(renderer))
scenes.append(SingleStepGradient(renderer))
scenes.append(PalRotate(renderer))
scenes.append(PixelPlane(renderer))
scenes.append(FirePlane(renderer))
scenes.append(GridBox(renderer))
world = CyclicWorld(scenes, window)



# ---------- main event (game) loop ---

print(" .. LEFT/RIGHT cycle through scenes")
print(" .. ESC quits")

running = True
while running:
  # [x] output - draw world
  world.process()
  # [x] input and [x] update the world
  events = lib.get_events()
  for e in events:
    if e.type == sdl2.SDL_QUIT:
      running = False
      break
    if e.type == sdl2.SDL_KEYDOWN:
      if e.key.keysym.sym == sdl2.SDLK_ESCAPE:
        running = False
        break
      if e.key.keysym.sym == sdl2.SDLK_LEFT:
        world.cycle(-1)
      if e.key.keysym.sym == sdl2.SDLK_RIGHT:
        world.cycle(1)

# /--------- main event (game) loop ---


lib.quit()  # /-- init ---

print("----------------// rainforce // 2014-2016 //--")
