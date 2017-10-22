import kivy
kivy.require('1.10.0')

from random import random
#kivy
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

# Set up background image and properties
class MyBackground(Widget):

    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        with self.canvas:
            self.bg = Rectangle(source='project.jpg', pos=self.pos, size=self.size)

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

# Define contents of graphical node
class ContentClass(GridLayout, Widget):
    def __init__(self, **kwargs):
        super(ContentClass, self).__init__(**kwargs)
        self.cols = 1
        self.slave = kwargs["slave"]

        self.nodemover = NodeMover(slave=self.slave, background_color=(0.8,0.8,0.8,0), text = "light", width = 1)
        self.textinput = TextInput(text="conf;g;g", background_color=(0.8,0.8,0.8,0.1), height=self.slave.size[1], width=100)

        self.add_widget(self.textinput)
        self.add_widget(self.nodemover)

    def get_text(self):
        return self.textinput.text

# Move node image
class NodeMover(Image):
    def __init__(self, **kwargs):
        super(NodeMover, self).__init__(**kwargs)
        self.slave = kwargs["slave"]

    def on_touch_down(self, touch):
        self.slave.on_touch_down_dummy(touch)

    def on_touch_move(self, touch):
        self.slave.on_touch_move_dummy(touch)

    def on_touch_up(self, touch):
        self.slave.on_touch_up_dummy(touch)

# Create graphical version of node
class GraphicalNode(GridLayout, ButtonBehavior, Image, Widget):

    def __init__(self, **kwargs):
        super(GraphicalNode, self).__init__(**kwargs)
        self.node = kwargs["node"]
        self.cols = 1
        self.txt = ContentClass(text="asdf", multiline=False, slave=self)
        self.center_x = 500
        self.add_widget(self.txt)

    # Activate node
    def on_touch_down_dummy(self, touch):
        #return
        if not self.parent.get_grapped() is None:
            return

        if touch.x < self.pos[0] or touch.x > self.pos[0] + self.size[0]:
            return
        if touch.y < self.pos[1] or touch.y > self.pos[1] + self.size[1]:
            return

        # Send configure if double click
        if touch.is_double_tap:
            # should there be other way to set conf besides sending the conf, no need at least as of yet
            self.node.set_conf(self.txt.get_text())
            self.node.send()

        self.parent.set_grapped(self)

    # Move node
    def on_touch_move_dummy(self, touch):

        if self.parent.get_grapped() is self:
            self.center_x = touch.x
            self.center_y = touch.y

    # Let go of node
    def on_touch_up_dummy(self, touch):

        if self.parent.get_grapped() is self:
            touch.ungrab(self)
            self.parent.set_grapped(None)

    # Return node
    def get_node(self):
        return self.node

class GraphicalUserInterface(App):

    def build(self):
        self.root = MyBackground()
        # this should not be required, cache issue, or what?
        GraphicalNode(source="light.gif", center_x=150, center_y=50, node=self)
        GraphicalNode(source="button.gif", center_x=150, center_y=50, node=self)
        GraphicalNode(source="unknown.gif", center_x=150, center_y=50, node=self)

        return self.root

    def get_root(self):
        return self.root
