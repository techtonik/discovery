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


try:
  import sdl2
except ImportError:
  # securely download PySDL2 (Windows only for now)
  import bootstrap
  import sdl2


# ---
# [x] create window of size ~500x100
#
# [ ] create game loop
#   [ ] output  - fill with pixels
#   [ ] input   - wait (for completion or until times comes)
#   [ ] process - recalculate pixel values
# /--


import sdl2.ext as lib

lib.init()  # --- init ---

window = lib.Window('HellFire', size=(500, 100))
window.show()


# --- main event (game) loop ---
# test event loop to see the window
lib.TestEventProcessor().run(window)
# /-- main event (game) loop ---


lib.quit()  # /-- init ---
