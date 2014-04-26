
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.label import Label

class UnderWorld(App):
  def build(self):
    return Label(text='Once upon a time..')


if __name__ == '__main__':
  UnderWorld().run()
