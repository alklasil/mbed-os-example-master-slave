from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock

from kivy.uix.togglebutton import ToggleButton
from kivy.core.clipboard import Clipboard

# popup class, shown when "more" clicked in the node in gui
class PopupClass(StackLayout, Widget):
    def __init__(self, **kwargs):
        super(PopupClass, self).__init__(**kwargs)
        self.slave = kwargs["slave"]
        self.infolabel = Label(text=self.slave.get_node().get_printable(c="\n", parse="everything"), color=(0.2,0.9,0.2,1), size_hint=(1, 0.4))
        self.backbutton = Button(text = "Back", background_color=(0.8,0.8,0.8,1), size_hint=(1, None))
        self.this_node_button = ToggleButton(text="This node", group="nodes", state='down', size_hint=(0.5, 0.1))
        self.all_nodes_button = ToggleButton(text="All nodes", group="nodes", size_hint=(0.5, 0.1))
        self.advertise_button = Button(text = "Force advertise", background_color=(0.8,0.8,0.8,1), size_hint=(0.5, 0.1))
        self.advertise1_button = Button(text = "Enable advertise", background_color=(0.8,0.8,0.8,1), size_hint=(0.5, 0.1))
        self.advertise0_button = Button(text = "Disable advertise", background_color=(0.8,0.8,0.8,1), size_hint=(0.5, 0.1))
        self.send_message_button = Button(text = "Force send_message", background_color=(0.8,0.8,0.8,1), size_hint=(0.5, 0.1))
        self.update_from_clipboard_button = Button(text = "Update from clipboard", background_color=(0.8,0.8,0.8,1), size_hint=(0.5, 0.1))

        self.add_widget(self.infolabel)
        self.add_widget(self.backbutton)
        self.add_widget(self.this_node_button)
        self.add_widget(self.all_nodes_button)
        self.add_widget(self.advertise_button)
        self.add_widget(self.send_message_button)
        self.add_widget(self.advertise1_button)
        self.add_widget(self.advertise0_button)
        self.add_widget(self.update_from_clipboard_button)

        self.infolabel_update_timestamp = self.slave.get_node().get_timestamp()
        def infolabel_update(_):
            if self.infolabel_update_timestamp != self.slave.get_node().get_timestamp():
                self.infolabel_update_timestamp = self.slave.get_node().get_timestamp()
                self.infolabel.text=self.slave.get_node().get_printable(c="\n", parse="everything")
        Clock.schedule_interval(infolabel_update, 1)

        self.selected_nodes = "this"
        def this_node_button_pressed(instance):
            self.selected_nodes = "this"
        def all_nodes_button_pressed(instance):
            self.selected_nodes = "all"

        def pre_msg():
            if self.selected_nodes == "this":
                return ""
            else:
                return "send_message;"

        def advertise_button_pressed(instance):
            self.slave.get_node().send(msg=pre_msg() + "advertise;")
        def advertise1_button_pressed(instance):
            self.slave.get_node().send(msg=pre_msg() + "advertise;s:1;")
        def advertise0_button_pressed(instance):
            self.slave.get_node().send(msg=pre_msg() + "advertise;s:0;")
        def send_message_button_pressed(instance):
            self.slave.get_node().send(msg=pre_msg() + "send_message;")
        def infolabel_on_touch_down(instance, touch):
            if self.selected_nodes == "this":
                text = "**PythonServer Clipboard**" + "\n"
                text = text + self.slave.get_node().get_printable(c="|", parse="essential", titles=False)
                Clipboard.copy(text)
            else:
                text = "**PythonServer Clipboard**" + "\n"
                for node in self.slave.get_node().get_nodelist().get_nodes():
                    if node.get_node_mode() != "DummyNode":
                        text = text + node.get_printable(c="|", parse="essential", titles=False)
                        text = text + "\n"
                Clipboard.copy(text)

        def update_from_clipboard_button_pressed(instance):
            self.slave.get_node().get_nodelist().update_from_text(
                node = self.slave.get_node(),
                text = Clipboard.paste(),
                selected_nodes = self.selected_nodes,
                gnode_parent = self.slave.get_parent()
            )


        self.this_node_button.bind(on_press=this_node_button_pressed)
        self.all_nodes_button.bind(on_press=all_nodes_button_pressed)
        self.advertise_button.bind(on_press=advertise_button_pressed)
        self.advertise1_button.bind(on_press=advertise1_button_pressed)
        self.advertise0_button.bind(on_press=advertise0_button_pressed)
        self.send_message_button.bind(on_press=send_message_button_pressed)
        self.infolabel.bind(on_touch_down=infolabel_on_touch_down)
        self.update_from_clipboard_button.bind(on_press=update_from_clipboard_button_pressed)


    def bind(self, bindTo):
        # used to bind the backbutton to close the popup when pressed
        self.backbutton.bind(on_press=bindTo)

class ContentClass(GridLayout, Widget):
    def __init__(self, **kwargs):
        super(ContentClass, self).__init__(**kwargs)
        self.cols = 1
        # content class's slave is GraphicalNode, maybe this should rather be named as master?
        self.slave = kwargs["slave"]

        self.sendbutton = Button(text = "Send", background_color=(0.8,0.8,0.8,0.7), size_hint_x=0.5)
        self.textinput = TextInput(text=self.slave.get_node().get_conf(), background_color=(0.8,0.8,0.8,0.7), multiline=False)
        self.morebutton = Button(text = "more", background_color=(0.8,0.8,0.8,0.7))
        self.nodemover = NodeMover(slave=self.slave, background_color=(0.8,0.8,0.8,0.5), size_hint_y=None, height=0)

        self.add_widget(self.sendbutton)
        self.add_widget(self.textinput)
        self.add_widget(self.morebutton)
        self.add_widget(self.nodemover)

        def on_focus(instance, value):
            # when the textinput loses focus, set the nodes conf_message (if begins with conf;), as it may have been modified
            if not value:
                if self.get_text().startswith('conf;'):
                    self.slave.get_node().set_conf(self.get_text())
        self.textinput.bind(focus=on_focus)

        def sendbutton_pressed(instance):
            # when send button pressed, send the node a message
            self.slave.get_node().send(msg=self.get_text())
        self.sendbutton.bind(on_press=sendbutton_pressed)

        def morebutton_pressed(instance):
            # when more-button pressed, create and open popup (see PopupClass)

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
            self.slave.get_parent().set_grapped(None)
        self.morebutton.bind(on_press=morebutton_pressed)

    def get_text(self):
        return self.textinput.text

    def set_text(self, text):
        self.textinput.text = text

class NodeMover(Image):
    # as textinput and on_touch cannot be in the same class
    # and the on_touch cannot be above textinput in hierarchy
    # we "need" NodeMover which forwards on_touch events to the GraphicalNode
    # this can be set to not be drawn (size = 0) and thus a viable option for now
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
        self.content = ContentClass(slave=self)
        self.add_widget(self.content)

    def on_touch_down_dummy(self, touch):
        # when the node is pressed, we set it grapped if no node is grapped as of yet
        if not self.parent.get_grapped() is None:
            return

        # check we did indeed click this particular node
        #     * There may be better ways of doing this
        #          (if so, do edit)
        if touch.x < self.pos[0] or touch.x > self.pos[0] + self.size[0]:
            return
        if touch.y < self.pos[1] or touch.y > self.pos[1] + self.size[1]:
            return

        # Tell the parent this node is grapped
        # prevents other nodes to be grapped at the same time
        #   (the nodes are checked in order -> we can no this as done here)
        #   (as only one instance of this function can be active at a time)
        self.parent.set_grapped(self)

    def on_touch_move_dummy(self, touch):

        # if this node is grapped and the mouse is moved, move the node
        if self.parent.get_grapped() is self:
            self.center_x = touch.x
            self.center_y = touch.y

    def on_touch_up_dummy(self, touch):

        # if the mouse is released, ungrap the node
        if self.parent.get_grapped() is self:
            self.parent.set_grapped(None)

    def get_node(self):
        # return the node this GraphicalNode belongs to
        return self.node

    def set_source(self, source):
        # set new image source
        # used when networkinterface receives new mode information about the node
        self.source=source

    def get_parent(self):
        # return the parent of the node. all nodes have the same parent.
        # the parent is the object the node is added as a widget to
        return self.parent

    def get_content(self):
        return self.content
