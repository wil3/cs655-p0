#import logging
#logging.getLogger("scapy.loading").setLevel(logging.CRITICAL)
#from scapy import *
import random

from packet import Packet

PKT_LEN_SIGMA = 20
pkt_counter = 0

class TrafficSource:

    def __init__(self,env,store,dport,src,dst):
        self.env = env
        self.store = store
        self.dport = dport
        self.src = src
        self.dst = dst 
        

    def tx(self, rate, len, var=False):
        """
        Transmit  packet, if var is true then 
        the len will be treated as the mean length
        and be sampled from exp distribution
        """
        
        global pkt_counter           
        seq = 0
        while pkt_counter < 10:
            if var:
                #this distri can return 0 so make sure its at least 1 bit
                l = int(random.expovariate(1.0/len)) + 1
            else:
                l = len
            pkt = self.build_pkt(l,seq)
            pkt_counter = pkt_counter + 1
            tx_delay = pkt.len/rate

            print pkt.src + "(" + str(pkt.len) + ")" + ">"
            yield self.env.timeout(tx_delay) #This symbolizes the transmission delay
            yield self.store.put(pkt) #And the packet added to the queue
            seq = seq + 1
#            print "[" + str(self.env.now) 
            
    def build_pkt(self,l, seq):
        p = Packet(self.src, self.dst, l, seq, self.dport)
        #l = random.gauss(mu_len,PKT_LEN_SIGMA)
      #  p = IP(dst=self.dst,src=self.src, len=l)/TCP(dport=self.dport, seq=self.seq)
        return p

    def __str__(self):
        return self.src + ":" + str(self.dport)
