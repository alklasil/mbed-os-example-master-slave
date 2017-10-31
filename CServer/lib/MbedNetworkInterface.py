#!/usr/bin/python
import socket
import ipaddress
import struct

import Node
import NodeList

UDP_IP = 'ff15::ABBA:ABBA'
UDP_IP_PACKED = ipaddress.ip_address(UDP_IP.decode('unicode-escape')).packed
UDP_PORT = 1234
OUDATE_TIME = 120
IP_LENGTH_USED = 14
#interface_index = socket.if_nametoindex('eth0')


class MbedNetworkInterface:

    def __init__(self):
        self.nodelist = NodeList.NodeList(self)

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


    def send(self, addr, nodes=None):
        print "networkinterface send"
        self.nodelist.send(self.sock, addr, nodes) # nodelis takes care if nodes in case nodes is None

    def sendMessage(self, msg="is_running=False", addr=UDP_IP, port=UDP_PORT):

#        print "sending message"
#
#        addrinfo = socket.getaddrinfo(UDP_IP, None)[0]
#
#        s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
#
#        # Set Time-to-live (optional)
#        ttl_bin = struct.pack('@i', 10)
#        if addrinfo[0] == socket.AF_INET: # IPv4
#            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
#        else:
#            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)

        print "sending: " + addr + " - " + msg
        try:
            self.sock.sendto(msg, (addr, port))
        except Exception as e: # TODO (better error handling and such)
            print e

    def serve(self, gnode_parent):
        print "serving"
        data, addr = self.sock.recvfrom(256)
        addr = addr[0]
        #addr = ipaddress.ip_address(addr.decode('unicode-escape')).exploded[-IP_LENGTH_USED:]
        print "received message:", data
        print "   sent by:", addr

        if "advertise:" in data:
            node_mode = data[len("advertise:"):]
            self.nodelist.update(addr, node_mode, gnode_parent)
        else:
            node_mode = "unknown"
            self.nodelist.update(addr, node_mode, gnode_parent)

    def get_nodelist(self):
        return self.nodelist

def main():
    networkInterface = MbedNetworkInterface()
    while True:
        networkInterface.run()

if __name__ == '__main__':
    main()
