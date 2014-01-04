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

__version__ = "0.1"

try:
  import sdl2
except ImportError:
  # securely download PySDL2 (Windows only for now)
  import bootstrap
  import sdl2


print("---------------------------[ demofire %s ]---" % __version__)

# ---
# [x] create window of size ~500x100
#
# [ ] create game loop
#   [ ] output  - fill with pixels
#   [ ] input   - wait (for completion or until times comes)
#   [ ] process - recalculate pixel values
#
# [ ] max FPS mode with measuring
# [ ] fixed FPS mode (25)
#   ---
#   [ ] measure CPU load for both
#   [ ] output results after window closed
#     [ ] optional mode with rendering on screen
# /--


import sdl2.ext as lib

lib.init()  # --- init ---

window = lib.Window('HellFire', size=(500, 100))
window.show()



# --- define world ---

class CyclicWorld(object):
  """world of strings"""

  def __init__(self, items):
    """every item is a string that is also a scene name"""
    if not items:
      raise ValueError("At least one element is required")
    self.items = items
    self.index = 0
    self.item = items[0]

  def cycle(self, count=1):
    """Count is any amount and can be negative"""
    self.index += count
    if self.index < 0 or self.index > len(self.items)-1:
      # modulo is a good operator for cycling in bounds
      self.index = self.index % len(self.items)
    self.item = self.items[self.index]

world = CyclicWorld('Yo! Hello, World of HellFire.'.split())

# --/ define world ---


# --- main event (game) loop ---

print(" .. LEFT/RIGHT cycle through scenes")
print(" .. ESC quits")

running = True
while running:
  # [x] output - draw world
  window.title = world.item
  # [x] input
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

  window.refresh()

# /-- main event (game) loop ---


lib.quit()  # /-- init ---

print("---------[ techtonik // rainforce // 2014 ]---")
