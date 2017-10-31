from kivy.uix.widget import Widget
import GraphicalNode

class Node:
    def __init__(self, timestamp, addr, node_mode, nodelist, gnode_parent=None):
        self.timestamp = timestamp
        self.addr = addr
        self.node_mode = node_mode
        self.is_running = True
        self.is_master = False
        self.is_slave = False # could be either slave or master (or master and slave, eg. light and button in the same device)
        self.nodelist = nodelist
        self.conf = "conf;g;g"

        self.gnode = GraphicalNode.GraphicalNode(color=(1,1,1,0.8), source="images/" + node_mode + ".gif", center_x=50, center_y=50, node=self)
        gnode_parent.add_widget(self.gnode)

    def get_nodelist(self):
        return self.nodelist

    def set_is_master(self, is_master=True):
        self.is_master = is_master

    def get_is_master(self):
        return self.is_master

    def set_is_slave(self, is_slave=True):
        self.is_slave = is_slave
        print "set is slave"

    def get_is_slave(self):
        return self.is_slave

    def clear_masters():
        pass

    def get_addr(self, length=0):
        if length <= 0 or length > len(self.addr):
            return self.addr

        return self.addr[-1 - len(self.addr) : -1]

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_node_mode(self):
        return self.node_mode

    def set_is_running(self, is_running):
        self.is_running = is_running

    def get_is_running(self):
        return self.is_running

    def get_conf(self):
        return self.conf

    def set_conf(self, conf="conf;g;g"):
        self.conf = conf

    def send(self, msg=None, addr=None):
        if msg is None: msg = self.conf
        if addr is None: addr = self.addr
        self.get_nodelist().get_networkInterface().sendMessage(msg=msg, addr=self.get_addr())

    def get_printable(self):
        return self.get_node_mode() + "; " + self.get_addr() + "; " + self.get_conf()
