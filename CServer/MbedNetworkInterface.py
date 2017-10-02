#!/usr/bin/python
import socket
import time
import ipaddress

UDP_IP = ""
UDP_PORT = 1234
OUDATE_TIME = 120
IP_LENGTH_USED = 14

class Node:
    def __init__(self, timestamp, addr, node_mode):
        self.timestamp = timestamp
        self.addr = addr
        self.node_mode = node_mode

    def get_addr(self):
        return self.addr

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_node_mode(self):
        return self.node_mode

class NodeList:

    def __init__(self):
        self.nodes = []

    def update(self, addr, node_mode):
        if not addr in (node.get_addr() for node in self.nodes):
            self.nodes.append(Node(int(time.time()), addr, node_mode))

    def removeOutdated(self):
        # remove outdated nodes
        timestamp = int(time.time())
        nodes_temp = self.nodes.copy()
        del self.nodes[:]
        for idx, node in self.nodes:
            if timestamp - node.get_timestamp() < OUDATE_TIME:
                self.nodes.append(node.copy())

    def show(self):
        print self.nodes

    def send(self, sock, addr, nodes=None):
        nodes = self.nodes if nodes == False else nodes
        msg = "set:set:master_buffer;" + (node.get_addr() for node in nodes)
        sock.sendto(msg, (addr, UDP_PORT))

    def toList():
        return ((node.get_addr(), node.get_node_mode()) for node in self.nodes)

    def get_nodes():
        return self.nodes

    def get_nodes_by_mode(self, mode):
        for node in self.nodes:
            if node.get_node_mode() is mode:
                yield node

class MbedNetworkInterface:

    def __init__(self):
        self.nodelist = NodeList()
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        #import struct
        #self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, "1" + "2")
        self.sock.bind((UDP_IP, UDP_PORT))
        
    def send(self, addr, nodes=None):
        self.nodelist.send(self.sock, addr, nodes if nodes == None else self.nodelist.get_nodes())

    def sendMessage(self, msg="is_running=False", addr="::1"):
        self.sock.sendto(msg, (addr, UDP_PORT))

    def serve(self):

        data, addr = self.sock.recvfrom(256)
        addr = addr[0]
        addr = ipaddress.ip_address(addr.decode('unicode-escape')).exploded[-IP_LENGTH_USED:]
        print "received message:", data
        print "   sent by:", addr

        if "advertise:" in data:
            node_mode = data[len("advertise:"):]
            self.nodelist.update(addr, node_mode)

    def get_nodelist(self):
        return self.nodelist

def main():
    networkInterface = MbedNetworkInterface()
    while True:
        networkInterface.run()

if __name__ == '__main__':
    main()    
