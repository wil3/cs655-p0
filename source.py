#import logging
#logging.getLogger("scapy.loading").setLevel(logging.CRITICAL)
#from scapy import *
import random
import q_algs
from packet import Packet

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
        seq = 0
        #Use a global variable to keep track of the 
        #total number of packets created so we can stop at the limit

        print q_algs.PKT_COUNTER
        while q_algs.PKT_COUNTER < q_algs.PKT_CREATE_MAX:
            print q_algs.PKT_COUNTER
            if var:
                #this distri can return 0 so make sure its at least 1 bit
                l = int(random.expovariate(1.0/len)) + 1
            else:
                l = len
            pkt = self.build_pkt(l,seq)
            q_algs.PKT_COUNTER = q_algs.PKT_COUNTER + 1
            tx_delay = pkt.len/rate

            print str(pkt.src) + "(" + str(pkt.len) + ")" + ">"
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
        return str(self.src) + ":" + str(self.dport)
