from GraphicalNode import GraphicalNode

class Node:
    def __init__(self, timestamp, addr, node_mode, nodelist, gnode_parent=None):
        self.timestamp = timestamp
        self.addr = addr
        self.node_mode = node_mode
        self.is_running = True
        self.nodelist = nodelist
        self.conf = "conf;g;g"

        if not gnode_parent is None:
            self.gnode = GraphicalNode(color=(1,1,1,0.8), source="images/" + node_mode + ".gif", center_x=50, center_y=50, node=self)
            gnode_parent.add_widget(self.gnode)

    def get_nodelist(self):
        return self.nodelist

    def get_gnode(self):
        return self.gnode

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

    def get_printable(self, c="; ", parse="essential"):
        if parse == "essential":
            return (
                  "mode: " + self.get_node_mode() + c
                + "addr: " + self.get_addr() + c
                + "conf: " + self.get_conf()
            )
        elif parse == "everything":
            return (
                  "mode: " + self.get_node_mode() + c
                + "addr: " + self.get_addr() + c
                + "conf: " + self.get_conf() + c
                + "timestamp: " + str(self.timestamp) + c
                + "is_running: " + str(self.is_running) + c
                + "last received: " + self.received
            )
        else:
            return "mode: " + self.get_node_mode()

    def set_received(self, received):
        self.received = received

    def get_received(self):
        return self.received