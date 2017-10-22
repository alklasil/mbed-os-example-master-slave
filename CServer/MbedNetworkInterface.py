#!/usr/bin/python
import socket
import time
import ipaddress
import struct

import GraphicalUserInterface

UDP_IP = 'ff15::ABBA:ABBA'
UDP_IP_PACKED = ipaddress.ip_address(UDP_IP.decode('unicode-escape')).packed
UDP_PORT = 1234
OUDATE_TIME = 120
IP_LENGTH_USED = 14
#interface_index = socket.if_nametoindex('eth0')

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

        # Create a graphical version of node
        self.gnode = GraphicalUserInterface.GraphicalNode(color=(1,1,1,0.4), source=node_mode +".gif", center_x=50, center_y=50, node=self)
        gnode_parent.add_widget(self.gnode)

    # Return list of nodes
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

    # Return node address
    def get_addr(self, length=0):
        if length <= 0 or length > len(self.addr):
            return self.addr

        return self.addr[-1 - len(self.addr) : -1]

    # Return node timestamp
    def get_timestamp(self):
        return self.timestamp

    # Return node timestamp
    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    # Return node mode ( "light", "button", "unknown" )
    def get_node_mode(self):
        return self.node_mode

    # Node to active/inactive ( True, False )
    def set_is_running(self, is_running):
        self.is_running = is_running

    # Return node state
    def get_is_running(self):
        return self.is_running

    # Return node configuration
    def get_conf(self):
        return self.conf

    # Set node configuration
    def set_conf(self, conf="conf;g;g"):
        self.conf = conf

    # Send message to device
    def send(self, msg=None, addr=None):
        if msg is None: msg = self.conf
        if addr is None: addr = self.addr
        self.get_nodelist().get_networkInterface().sendMessage(msg=msg, addr=self.get_addr())

    def get_printable(self):
        return self.get_node_mode() + "; " + self.get_addr() + "; " + self.get_conf()

class NodeList:

    def __init__(self, networkInterface):
        self.nodes = []
        self.networkInterface = networkInterface

    # Return network interface
    def get_networkInterface(self):
        return self.networkInterface

    # Update nodelist
    def update(self, addr, node_mode, gnode_parent):
        timestamp = int(time.time())
        found = False
        for node in self.nodes:
            print "-" + addr + "-VS-" + node.get_addr() + "-"
            if addr == node.get_addr():
                print "exist"
                node.set_is_running(True)
                node.set_timestamp(timestamp)
                # update also image here (TODO)
                found = True
                break
        if not found:
            # Add new node to list
            self.nodes.append(Node(timestamp, addr, node_mode, self, gnode_parent))

    # Remove outdated nodes
    def removeOutdated(self):
        timestamp = int(time.time())
        for idx, node in self.nodes:
            if node.is_running:
                if timestamp - node.get_timestamp() > OUDATE_TIME:
                    node.set_is_running(False)

    # Print list of current nodes
    def show(self):
        print self.nodes

    # Send message
    def send(self, sock, addr, nodes=None):
        if nodes is None:
            nodes = self.nodes
        msg = "master;" + (node.get_addr(length=24) + ";" for node in nodes)
        print 'sent:' + msg
        sock.sendto(msg, (addr, UDP_PORT))

    def toList():
        return ((node.get_addr(), node.get_node_mode()) for node in self.nodes)

    # Return list of nodes
    def get_nodes():
        return self.nodes

    # Return all nodes of a mode
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

class MbedNetworkInterface:

    def __init__(self):
        self.nodelist = NodeList(self)

        addrinfo = socket.getaddrinfo(UDP_IP, None)[0]

        # Create a socket
        self.sock = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind it to the port
        self.sock.bind(('', UDP_PORT))

        group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
        
        # Join group
        mreq = group_bin + struct.pack('@I', 0)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        print "connected"

    # Send message (to nodes on list?)
    def send(self, addr, nodes=None):
        print "networkinterface send"
        self.nodelist.send(self.sock, addr, nodes) # nodelist takes care if nodes in case nodes is None

    # Send message (to mesh?)
    def sendMessage(self, msg="is_running=False", addr=UDP_IP, port=UDP_PORT):
        print "sending: " + addr + " - " + msg
        try:
            self.sock.sendto(msg, (addr, port))
        except Exception as e: # TODO (better error handling and such)
            print e

    # Handle advertisements from devices
    def serve(self, gnode_parent):
        print "serving"
        # Receive data from device
        data, addr = self.sock.recvfrom(256)
        addr = addr[0]
        #addr = ipaddress.ip_address(addr.decode('unicode-escape')).exploded[-IP_LENGTH_USED:]
        print "received message:", data
        print "   sent by:", addr

        # Update the node state
        if "advertise:" in data:
            node_mode = data[len("advertise:"):]
            self.nodelist.update(addr, node_mode, gnode_parent)
        else:
            node_mode = "unknown"
            self.nodelist.update(addr, node_mode, gnode_parent)

    # Return list of nodes
    def get_nodelist(self):
        return self.nodelist

def main():
    networkInterface = MbedNetworkInterface()
    while True:
        networkInterface.run()

if __name__ == '__main__':
    main()
