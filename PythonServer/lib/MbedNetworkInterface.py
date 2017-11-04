#!/usr/bin/python
import socket
import ipaddress
import struct

from NodeList import NodeList

UDP_IP = 'ff15::ABBA:ABBA'
UDP_IP_PACKED = ipaddress.ip_address(UDP_IP.decode('unicode-escape')).packed
UDP_PORT = 1030
OUDATE_TIME = 120
IP_LENGTH_USED = 14


class MbedNetworkInterface:

    def __init__(self):
        self.nodelist = NodeList(self)

        addrinfo = socket.getaddrinfo(UDP_IP, None)[0]

        # Create a socket
        self.sock = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket
        self.sock.bind(('', UDP_PORT))

        # Join a group
        group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
        mreq = group_bin + struct.pack('@I', 0)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        print("connected")


    def send(self, addr, nodes=None):
        print("networkinterface send")
        self.nodelist.send(self.sock, addr, nodes) # nodelis takes care if nodes in case nodes is None

    def sendMessage(self, msg="is_running=False", addr=UDP_IP, port=UDP_PORT):

        print("sending: ", addr, " - ", msg)
        try:
            self.sock.sendto(msg, (addr, port))
        except Exception as e: # TODO (better error handling and such)
            print e

    def serve(self, gnode_parent):
        print("serving")
        data, addr = self.sock.recvfrom(256)
        addr = addr[0]
        print("received message:", data)
        print("   sent by:", addr)

        if "#advertise:" in data:
            node_mode = data[len("#advertise:"):data.index(';')]
            node_state = 1 if "s:1;" in data else 0 # add this to nodes attrs when adding visual
            self.nodelist.update(data, addr, node_mode, gnode_parent)
        else:
            node_mode = "unknown"
            self.nodelist.update(data, addr, node_mode, gnode_parent)

    def get_nodelist(self):
        return self.nodelist

    def get_outdate_time(self):
        return OUDATE_TIME

def main():
    networkInterface = MbedNetworkInterface()
    while True:
        networkInterface.run()

if __name__ == '__main__':
    main()
