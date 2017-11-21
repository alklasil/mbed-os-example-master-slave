import time
from lib.Node import Node

class NodeList:
    # this class is used to store the nodes in a particular MbedNetworkInterface
    # this class acts as a bridge between the Nodes and the MbedNetworkInterface
    #    to which they are "connected" to
    # list may not be such a great structure in the end, should be easy to change

    def __init__(self, networkInterface):
        self.nodes = []
        self.networkInterface = networkInterface

    def get_networkInterface(self):
        return self.networkInterface

    def update(self, data, addr, node_mode, gnode_parent, conf=None):
        # when the MbedNetworkInterface receives message
        # the Nodelist checks whether the from which the message was received is already
        # a member or not, if not the Node is added, if yes, the Node is updated
        timestamp = int(time.time())
        _node = None
        if self.nodes:
            for node in self.nodes:
                print ("-", addr, "-VS-", node.get_addr(), "-")
                if addr == node.get_addr():
                    # node is already in nodelist -> update
                    print ("node exist")
                    node.set_is_running(True)
                    node.set_timestamp(timestamp)
                    # for now only change node_mode once from unknown to something else
                    # if node could change its mode (in the future perhaps), edit this
                    if node.get_node_mode() != node_mode and data.startswith('#advertise:'):
                        node.get_gnode().set_source("images/" + node_mode + ".gif")
                        node.set_node_mode(node_mode)
                    _node = node
                    break
        if _node is None:
            # node did not exist yet -> create new node and add it to the list
            _node = Node(timestamp, addr, node_mode, self, gnode_parent)
            self.nodes.append(_node)
        _node.set_received(data)
        if conf != None:
            # usually the nodes do not send their configuration when advertising
            #   (at least for now, thus conf=None -> default configuration)
            #   (see Node.py for more detail)
            # otherwise (the function is called elsewhere)
            #           (and conf is given as parameter, then set the nodes conf)
            _node.set_conf(conf)
        return _node

    def update_from_text(self, node, text, selected_nodes, gnode_parent):
        try:
            lines = text.splitlines()
            if lines[0] == '**PythonServer Clipboard**':
                lines = lines[1:]
                data = [line.split('|') for line in lines]

                # mode|addr|conf
                # mode|addr|conf
                # ...
                if selected_nodes == "this":
                    for mode, addr, conf, center in data:
                        if addr == node.get_addr():
                            _node = self.update(
                                "#advertise:(update from clipboard)", addr, mode, gnode_parent, conf
                            )
                            center_x, center_y = center.split(":")
                            _node.get_gnode().center_x = float(center_x)
                            _node.get_gnode().center_y = float(center_y)
                else:
                    for mode, addr, conf, center in data:
                        _node = self.update(
                            "#advertise:(update from clipboard)", addr, mode, gnode_parent, conf
                        )
                        center_x, center_y = center.split(":")
                        _node.get_gnode().center_x = float(center_x)
                        _node.get_gnode().center_y = float(center_y)
            else:
                print("Data illformatted when updating from clipboard:"), text
        except:
            # no matter what exception happens when pasting from clipboard
            # let's not let it shut the threads down
            #    (for now handle the execptions very simply)
            pass

    def removeOutdated(self):
        # remove outdated nodes
        timestamp = int(time.time())
        if self.nodes:
            for node in self.nodes:
                if node.is_running:
                    if timestamp - node.get_timestamp() > self.networkInterface.get_outdate_time():
                        node.set_is_running(False)

    def get_nodes(self):
        return self.nodes

    def get_nodes_by_mode(self, mode):
        # this may be wanted if ordering the nodes based on mode for some reason
        for node in self.nodes:
            if node.get_node_mode() is mode:
                yield node
