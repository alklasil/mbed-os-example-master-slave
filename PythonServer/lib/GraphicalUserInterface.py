import os

from kivy.config import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.uix.image import Image


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

    def get_size(self):
        return self.size


class GraphicalUserInterface(App):

    def build(self):
        self.root = MyBackground()
        for file in os.listdir("images"):
            if file.endswith(".gif"):
                Image(source="images/" + file)
        return self.root

    def get_root(self):
        return self.root
