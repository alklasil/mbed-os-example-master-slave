#!/usr/bin/python
import socket
import ipaddress
import struct

from lib.NodeList import NodeList

# network variables (add these inside the MbedNetworkInterface?)
# (-> multiple instances of MbedNetworkInterface with different network variables)
# (in the same instance of the program could be used. or set these as commandlinearguments?)
UDP_IP = 'ff15::ABBA:ABBA'
UDP_IP_PACKED = ipaddress.ip_address(UDP_IP.decode('unicode-escape')).packed
UDP_PORT = 1030
OUDATE_TIME = 120
IP_LENGTH_USED = 14


class MbedNetworkInterface:
    # interface for accessing the network
    # from backhaul network (UI) to the mbed network

    def __init__(self):
        # create nodelist which will store all the information of the (visible)
        # nodes present in the mbed network
        # give the nodelist MbedNetworkInterface as argument
        #  (could create multiple NodeLists with different MbedNetworkInterfaces)
        self.nodelist = NodeList(self)

        # Create a socket
        addrinfo = socket.getaddrinfo(UDP_IP, None)[0]
        self.sock = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket
        self.sock.bind(('', UDP_PORT))

        # Join the group
        group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
        mreq = group_bin + struct.pack('@I', 0)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        print("instance of MbedNetworkInterface created and connected")

    def sendMessage(self, msg="is_running=False", addr=UDP_IP, port=UDP_PORT):
        print("sending: ", addr, " - ", msg)
        try:
            self.sock.sendto(msg, (addr, port))
        except Exception as e: # TODO (better error handling and such)
            print(e)

    def serve(self, gnode_parent):
        data, addr = self.sock.recvfrom(256)
        addr = addr[0]
        if '\x00' in data:
            data = data[:data.index('\x00')]
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
