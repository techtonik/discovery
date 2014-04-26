
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

intro = """\
Once upon a time..
..there was a story..
..of mighty warrior..
..who was...
..actually a jerk..
..because he didn't want..
..to save a princess..
..captured..
..in the UnderWorld.
"""

class TouchyScreenManager(ScreenManager):
  def on_touch_down(self, touch):
    next = self.next()
    self.current = next


class UnderWorld(App):
  def build(self):
    self.sm = TouchyScreenManager()
    for storyline in intro.splitlines():
      screen = Screen(name=storyline)
      screen.add_widget(Label(text=storyline))
      self.sm.add_widget(screen)
    return self.sm


if __name__ == '__main__':
  UnderWorld().run()
