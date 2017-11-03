from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
import TestEnvironment

class PopupClass(StackLayout, Widget):
    def __init__(self, **kwargs):
        super(PopupClass, self).__init__(**kwargs)
        self.slave = kwargs["slave"]
        self.backbutton = Button(text = "Back", background_color=(0.8,0.8,0.8,1), size_hint=(0.5, None))
        self.testbutton = Button(text = "Run diagnosis\n[experimental]", background_color=(0.8,0.8,0.8,1), size_hint=(0.5, None))
        self.infolabel = Label(text=self.slave.get_node().get_printable("\n"), color=(0.2,0.9,0.2,1), size_hint=(1, 0.4))


        self.add_widget(self.infolabel)
        self.add_widget(self.testbutton)
        self.add_widget(self.backbutton)
        def testbutton_pressed(instance):
            self.slave.get_node().test()
        self.testbutton.bind(on_press=testbutton_pressed)

    def bind(self, bindTo):
        self.backbutton.bind(on_press=bindTo)

class ContentClass(GridLayout, Widget):
    def __init__(self, **kwargs):
        super(ContentClass, self).__init__(**kwargs)
        self.cols = 1

        self.slave = kwargs["slave"]

        self.sendbutton = Button(text = "Send", background_color=(0.8,0.8,0.8,0.7))
        self.textinput = TextInput(text="conf;g;g", background_color=(0.8,0.8,0.8,0.7), multiline=False)
        self.morebutton = Button(text = "more", background_color=(0.8,0.8,0.8,0.7))
        self.nodemover = NodeMover(slave=self.slave, background_color=(0.8,0.8,0.8,0.5), size_hint_y=None, height=0)

        self.add_widget(self.sendbutton)
        self.add_widget(self.textinput)
        self.add_widget(self.morebutton)
        self.add_widget(self.nodemover)

        def on_focus(instance, value):
            if not value:
                self.slave.get_node().set_conf(self.get_text())
        self.textinput.bind(focus=on_focus)

        def sendbutton_pressed(instance):
            self.slave.get_node().set_conf(self.get_text())
            self.slave.get_node().send()
        self.sendbutton.bind(on_press=sendbutton_pressed)

        def morebutton_pressed(instance):
            # create content and add to the popup
            content = PopupClass(slave=self.slave)
            popup = Popup(
                content=content,
                title="GraphicalNode Popup",
                auto_dismiss=False,
                size_hint=(None, None),
                size=(
                    self.slave.get_parent().get_size()[0] * 0.8,
                    self.slave.get_parent().get_size()[1]
                )
            )
            content.bind(popup.dismiss)
            popup.open()
        self.morebutton.bind(on_press=morebutton_pressed)

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
            # save node data
            self.node.set_conf(self.content.get_text())

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

    def get_parent(self):
        return self.parent
