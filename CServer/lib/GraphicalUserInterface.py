import kivy
kivy.require('1.10.0')

from random import random
#kivy
from kivy.config import Config
Config.set('graphics','width',960)
Config.set('graphics','height',480)
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.textinput import FocusBehavior
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.input.motionevent import MotionEvent
import GraphicalNode


class MyBackground(Widget):

    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        with self.canvas:
            self.bg = Rectangle(source='images/project.gif', pos=self.pos, size=self.size)
            #self.add_widget(TextInput(text="HELLO WORLD", focus=True))

        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)
        self.set_grapped(None)

    def set_grapped(self, grapped):
        self.grapped = grapped

    def get_grapped(self):
        return self.grapped

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def save(self):
        pass

    def load(self):
        pass


class GraphicalUserInterface(App):

    def build(self):
        self.root = MyBackground()
        # this should not be required, cache issue, or what?
        GraphicalNode.GraphicalNode(source="images/light.gif", center_x=150, center_y=50, node=self)
        GraphicalNode.GraphicalNode(source="images/button.gif", center_x=150, center_y=50, node=self)
        GraphicalNode.GraphicalNode(source="images/unknown.gif", center_x=150, center_y=50, node=self)
        #self.root.add_widget(gnode)
        return self.root

    def get_root(self):
        return self.root
