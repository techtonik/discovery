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

__version__ = "0.7"

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


# --- helpers ---

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


# --- init ---

import sdl2.ext as lib

lib.init()

window = lib.Window('HellFire', size=(WIDTH, HEIGHT))
window.show()

# renderer knows how to draw in a window, it provides
# universal interface to update window contents regardless
# of window type (GDI, OpenGL, ...)
renderer = lib.RenderContext(window)


# --- define world ---
#
# world of scenes
#
# every scene is an algorithm that produces fire

class Scene(object):
  """scene knows about renderer and draws itself, it
     doesn't know anything about window (except size)"""

  def __init__(self, title, renderer):
    self.title = title    # scene / algoritm name
    #self.renderer = renderer

  def draw(self):
    """called from main loop to draw frame"""
    pass

  def switch(self):
    """method called on scene switch"""
    pass


class PixelScene(Scene):
  def draw(self):
    renderer.draw_point([10,10], lib.Color(255,255,255))
    renderer.present()

  def switch(self):
    renderer.clear()

from random import randint
class PixelLine(Scene):
  def __init__(self, title, renderer):
    Scene.__init__(self, title, renderer)
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
  def __init__(self, title, renderer):
    Scene.__init__(self, title, renderer)
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


class FPS(object):
  def __init__(self):
    self.counter = 0
    self.timer = Timer(1)
  def process(self):
    self.counter += 1
    if self.timer.expired:
      print "FPS: %s" % self.counter
      self.counter = 0
      self.timer.restart()


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

# generate some empty scenes
names = ['Yo! Press Left to continue...']
names.extend('Hello, World of HellFire.'.split())
scenes = [Scene(name, renderer) for name in names]
# add first scene with *real* content
scenes.append(PixelScene('[A Pixel from Hell]', renderer))
# add scene that draws lines
scenes.append(PixelLine('[Lines of Pixel]', renderer))
# add scene that draws lines by lines
scenes.append(LineLine('[Lines by Line]', renderer))
world = CyclicWorld(scenes, window)

# --/ define world ---


# --- main event (game) loop ---

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

# /-- main event (game) loop ---


lib.quit()  # /-- init ---

print("---------[ techtonik // rainforce // 2014 ]---")
