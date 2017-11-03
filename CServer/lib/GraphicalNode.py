from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button

import TestEnvironment

class ContentClass(GridLayout, Widget):
    def __init__(self, **kwargs):
        super(ContentClass, self).__init__(**kwargs)
        self.cols = 1

        self.slave = kwargs["slave"]

        self.textinput = TextInput(text="conf;g;g", background_color=(0.8,0.8,0.8,0.1))
        self.run_tests_button = Button(text = "run_tests", background_color=(0.8,0.8,0.8,0.7))
        self.nodemover = NodeMover(slave=self.slave, background_color=(0.8,0.8,0.8,0.5), size_hint_y=None, height=0)
        #self.send_button = Button(text="Send", background_color=(1,1,1,0.1), color=(0,0,0,1))

        self.add_widget(self.textinput)
        self.add_widget(self.nodemover)
        self.add_widget(self.run_tests_button)
        import threading
        def run_tests_button_pressed(instance):
            #TestEnvironment.TestEnvironment().run_tests(self.slave.get_node())).start()
            self.slave.get_node().test()

        self.run_tests_button.bind(on_press=run_tests_button_pressed)

    def get_text(self):
        return self.textinput.text

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

class GraphicalNode(GridLayout, Image, Widget):

    def __init__(self, **kwargs):
        super(GraphicalNode, self).__init__(**kwargs)
        self.node = kwargs["node"]
        self.cols = 1
        self.content = ContentClass(text="asdf", multiline=True, slave=self)
        self.center_x = 500
        self.add_widget(self.content)

    #def on_touch_down(self, touch):
    def on_touch_down_dummy(self, touch):
        #return
        if not self.parent.get_grapped() is None:
            return

        if touch.x < self.pos[0] or touch.x > self.pos[0] + self.size[0]:
            return
        if touch.y < self.pos[1] or touch.y > self.pos[1] + self.size[1]:
            return

        if touch.is_double_tap:
            # should there be other way to set conf besides sending the conf, no need at least as of yet
            self.node.set_conf(self.content.get_text())
            self.node.send()

        self.parent.set_grapped(self)

    #def on_touch_move(self, touch):
    def on_touch_move_dummy(self, touch):

        if self.parent.get_grapped() is self:
            self.center_x = touch.x
            self.center_y = touch.y

    #def on_touch_up(self, touch):
    def on_touch_up_dummy(self, touch):

        if self.parent.get_grapped() is self:
            touch.ungrab(self)
            self.parent.set_grapped(None)

    def get_node(self):
        return self.node

    def set_source(self, source):
        self.source=source
