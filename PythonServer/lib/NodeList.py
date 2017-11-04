import time
from Node import Node

class NodeList:

    def __init__(self, networkInterface):
        self.nodes = []
        self.networkInterface = networkInterface

    def get_networkInterface(self):
        return self.networkInterface

    def update(self, data, addr, node_mode, gnode_parent):
        timestamp = int(time.time())
        _node = None
        for node in self.nodes:
            print ("-", addr, "-VS-", node.get_addr(), "-")
            if addr == node.get_addr():
                print ("node exist")
                node.set_is_running(True)
                node.set_timestamp(timestamp)
                if (node.get_gnode().get_node().get_node_mode() == "unknown"):
                    node.get_gnode().set_source("images/" + node_mode + ".gif")
                _node = node
                break
        if _node is None:
            _node = Node(timestamp, addr, node_mode, self, gnode_parent)
            self.nodes.append(_node)
        _node.set_received(data) # FIXME: perhaps only when testing?

    def removeOutdated(self):
        # remove outdated nodes
        timestamp = int(time.time())
        for idx, node in self.nodes:
            if node.is_running:
                if timestamp - node.get_timestamp() > OUDATE_TIME:
                    node.set_is_running(False)

    def show(self):
        print self.nodes

    def toList():
        return ((node.get_addr(), node.get_node_mode()) for node in self.nodes)

    def get_nodes():
        return self.nodes

    def get_nodes_by_mode(self, mode):
        for node in self.nodes:
            if node.get_node_mode() is mode:
                yield node

    def get_slave_nodes(self):
        for node in self.nodes:
            if node.get_is_master():
                yield node

    def get_master_nodes(self):
        for node in self.nodes:
            if node.get_is_slave():
                yield node
