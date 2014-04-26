
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

intro = """\
Once upon a time..
..there was a story..
...
"""

class UnderWorld(App):
  def build(self):
    self.sm = ScreenManager()
    for storyline in intro.splitlines():
      screen = Screen(name=storyline)
      screen.add_widget(Label(text='Once upon a time..'))
      self.sm.add_widget(screen)
    return self.sm


if __name__ == '__main__':
  UnderWorld().run()
