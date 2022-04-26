####################################################
# DVrouter
# Name: Alexander Rosenthal
# BU ID: U87066904
#####################################################

import sys
from collections import defaultdict
from router import Router
from packet import Packet
from json import dumps, loads


class DVrouter(Router):
    """Distance vector routing protocol implementation."""

    def __init__(self, addr, heartbeatTime):
        """init"""
        Router.__init__(self, addr)  # initialize superclass 
        self.heartbeatTime = heartbeatTime
        self.last_time = 0
        # initialize local state
        pass

    def handlePacket(self, port, packet):
        """process incoming packet"""
        if packet.isTraceroute():
            # if the forwarding table contains packet.dstAddr
            #   send packet based on forwarding table, e.g., self.send(port, packet)
            pass
        else:
            # if the received distance vector is different
            #   update the local copy of the distance vector
            #   update the distance vector of this router
            #   update the forwarding table
            #   broadcast the distance vector of this router to neighbors
            pass


    def handleNewLink(self, port, endpoint, cost):
        """handle new link"""
        # update the distance vector of this router
        # update the forwarding table
        # broadcast the distance vector of this router to neighbors
        pass


    def handleRemoveLink(self, port):
        """handle removed link"""
        # update the distance vector of this router
        # update the forwarding table
        # broadcast the distance vector of this router to neighbors
        pass


    def handleTime(self, timeMillisecs):
        """handle current time"""
        if timeMillisecs - self.last_time >= self.heartbeatTime:
            self.last_time = timeMillisecs
            # broadcast the distance vector of this router to neighbors
            pass


    def debugString(self):
        """generate a string for debugging in network visualizer"""
        return ""
