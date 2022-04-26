####################################################
# LSrouter
# Name: Alexander Rosenthal
# BU ID: U87066904
#####################################################

import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from router import Router
from packet import Packet
from json import dumps, loads


class LSrouter(Router):
    """Link state routing protocol implementation."""

    def __init__(self, addr, heartbeatTime):
        """init"""
        Router.__init__(self, addr)  # initialize superclass 
        self.heartbeatTime = heartbeatTime
        self.last_time = 0

        #creating network graph
        self.G = nx.Graph()
        self.G.add_node(addr)
        self.key = []
        self.update = 0
        self.alllinks = [0]*26
        self.linkversions = [0]*26


      
        pass


    def handlePacket(self, port, packet):
        """process incoming packet"""
        if packet.isTraceroute():
            # if the forwarding table contains packet.dstAddr
            #   send packet based on forwarding table, e.g., self.send(port, packet)

            #sort through self link state and find the source of packet
            for pair in self.key:
                if pair[0] == port:
                    src = pair[1]

            #try to find a shortest path from current router to dest router
            try:
                #find shortest path
                path = nx.dijkstra_path(self.G,self.addr,packet.dstAddr)
                #look for next step in path and find corresponding port to send
                for pair in self.key:
                    if pair[1] == path[1]:
                        # print(pair)
                        next = pair[0]
                        # print('next step', pair[1])
                self.send(next, packet)


            except:
                # print("no path yet")
                pass

            pass
        else:
            # check the sequence number
            # if the sequence number is higher and the received link state is different
            #   update the local copy of the link state
            #   update the forwarding table
            #   broadcast the packet to other neighbors

            
            msg = json.loads(packet.content)            
            # check seq num and update global linkstate list and linkstate version list
            if msg[-1][-2] > self.linkversions[ord(msg[-1][-1])-65]:
                self.linkversions[ord(msg[-1][-1])-65] = msg[-1][-2]
                self.alllinks[ord(msg[-1][-1])-65] = msg

                #clear old graph
                self.G.clear()

                #build new graph from new global linkstate list
                for el in self.alllinks:
                    try:
                        for state in el:
                            self.G.add_edge(state[4],state[1],weight=state[2])
                    except:
                        pass

                for pair in self.key:
                    if pair[0] != port:
                        self.send(pair[0],packet)
    
                # #get pkt content and update graph
                # for pair in msg:
                #     self.G.add_edge(pair[4], pair[1], weight = pair[2])
                # for pair in self.key:
                #     if pair[0] != port:
                #         self.send(pair[0],packet)


            pass


    def handleNewLink(self, port, endpoint, cost):
        """ handle new link"""
        # update the forwarding table
        # broadcast the new link state of this router to all neighbors

        #update port addr dict
        self.update+=1
        self.linkversions[ord(self.addr)-65] = self.update
        self.key.append([port,endpoint,cost,self.update,self.addr])
        self.alllinks[ord(self.addr)-65] = self.key
        #print(self.alllinks[ord(self.addr)-65][-1][-2])


        #add new node and edge to graph
        self.G.add_node(endpoint)
        self.G.add_edge(self.addr, endpoint, weight = cost)

        
        #create and send routing packets to neighbors
        for pair in self.key:
            source = self.addr
            dest = pair[1]
            msg = json.dumps(self.key)
            p = Packet(kind = Packet.ROUTING, srcAddr = source, dstAddr = dest, content = msg)
            self.send(pair[0],p)
        pass


    def handleRemoveLink(self, port):
        """ handle removed link"""
        # update the forwarding table
        # broadcast the new link state of this router to all neighbors

        #delete old link from link state
        self.update+=1
        self.linkversions[ord(self.addr)-65] = self.update
        for states in self.key:
            if states[0] == port:
                self.G.remove_edge(self.addr,states[1])
                self.key.remove(states)

        #update global link state list
        self.alllinks[ord(self.addr)-65] = self.key
        #add seq num to new packet
        self.key[-1][-2] = self.update
        
        
        #create and send routing packets to neighbors
        
        for pair in self.key:
            source = self.addr
            dest = pair[1]
            msg = json.dumps(self.key)
            p = Packet(kind = Packet.ROUTING, srcAddr = source, dstAddr = dest, content = msg)
            #print("send update from to", self.addr, pair[1])
            self.send(pair[0],p)


        pass


    def handleTime(self, timeMillisecs):
        """ handle current time"""
        if timeMillisecs - self.last_time >= self.heartbeatTime:
            self.last_time = timeMillisecs
            # Hints:
            # broadcast the link state of this router to all neighbors
            for pair in self.key:
                source = self.addr
                dest = pair[1]
                msg = json.dumps(self.key)
                p = Packet(kind = Packet.ROUTING, srcAddr = source, dstAddr = dest, content = msg)
                self.send(pair[0],p)
            pass


    def debugString(self):
        """ generate a string for debugging in network visualizer"""
        #return nx.info(self.G,self.addr)
        #return nx.info(self.G)
        xx = list(self.G.neighbors(self.addr))
        return str(xx)



















