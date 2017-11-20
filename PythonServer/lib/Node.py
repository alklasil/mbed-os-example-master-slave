from lib.GraphicalNode import GraphicalNode

class Node:
    # this class stores data about a node
    # acts also as a interface to the physical counterpart

    def __init__(self, timestamp, addr, node_mode, nodelist, gnode_parent=None):
        # set initial values
        self.timestamp = timestamp
        self.addr = addr
        self.node_mode = node_mode
        self.is_running = True
        self.nodelist = nodelist
        self.conf = "conf;g;g;"

        # Add GraphicalNode if gnode_parent (GraphicalUserInterface.root) exists
        if not gnode_parent is None:
            # create GraphicalNode and set node=self (-> GraphicalNode contains link to this node)
            self.gnode = GraphicalNode(color=(1,1,1,0.8), source="images/" + node_mode + ".gif", center_x=500, center_y=50, node=self)
            gnode_parent.add_widget(self.gnode)

    def get_nodelist(self):
        # get nodelist to which this node belongs to
        return self.nodelist

    def get_gnode(self):
        # get the GraphicalNode(node=self)
        return self.gnode

    def get_addr(self, length=0):
        if length <= 0 or length > len(self.addr):
            return self.addr

        return self.addr[-1 - len(self.addr) : -1]

    def get_timestamp(self):
        # timestamp is used to keep track when the node was last heard of
        # i.e., if the node outdated or not
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_node_mode(self):
        return self.node_mode

    def set_node_mode(self, node_mode):
        self.node_mode = node_mode

    def set_is_running(self, is_running):
        # if is_running is False, the node may or may not be running, but we do
        # not know whether it is running.
        # here we could send the physical node a #advertise yourself message
        # to update it's state and determine whether it actually is running or not
        self.is_running = is_running

    def get_is_running(self):
        return self.is_running

    def get_conf(self):
        return self.conf

    def set_conf(self, conf="conf;g;g;"):
        self.conf = conf
        self.gnode.get_content().set_text(self.conf)

    def send(self, msg=None, addr=None):
        # send message to the physical node. default message is the conf message
        # add possibilty to the gui to send other messages without modifying
        # the conf-message
        if msg is None: msg = self.conf
        if addr is None: addr = self.addr
        self.get_nodelist().get_networkInterface().sendMessage(msg=msg, addr=self.get_addr())

    def get_printable(self, c="; ", parse="essential", titles=True):

        if titles:
            t = 1
        else:
            t = 0

        if parse == "essential":
            return (
                  t * "mode: "  + self.get_node_mode() + c
                + t * "addr: " + self.get_addr() + c
                + t * "conf: " + self.get_conf() + c
                + t * "center: " + str(self.gnode.center_x) + ":" + str(self.gnode.center_y)
            )
        elif parse == "everything":
            return (
                  self.get_printable(c, "essential", titles) + c
                + t * "timestamp: " + str(self.timestamp) + c
                + t * "is_running: " + str(self.is_running) + c
                + t * "last received: " + self.received
            )
        else:
            return t * "mode: " + self.get_node_mode()

    def set_received(self, received):
        self.received = received

    def get_received(self):
        return self.received

    def save(self):
        pass

    def load(self):
        pass
