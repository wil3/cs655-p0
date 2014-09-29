import logging
logging.getLogger("scapy.loading").setLevel(logging.CRITICAL)
from scapy import *
import random
"""

"""
PKT_LEN_SIGMA = 20
class TrafficSource:

    def __init__(self,env,store,dport,src,dst):
        self.env = env
        self.store = store
        self.dport = dport
        self.src = src
        self.dst = dst 
        self.seq = 0


    def tx(self, rate, len, var=False):
        """
        Transmit  packet, if var is true then 
        the len will be treated as the mean length
        and be sampled from exp distribution
        """
        while 1:
            if var:
                #this distri can return 0 so make sure its at least 1 bit
                l = int(random.expovariate(1.0/len)) + 1
            else:
                l = len
            pkt = self.build_pkt(l)
            tx_delay = pkt.len/rate
            yield self.env.timeout(tx_delay)
            yield self.store.put(pkt)
            self.seq = self.seq + 1

    def build_pkt(self,l):

        #l = random.gauss(mu_len,PKT_LEN_SIGMA)
        p = IP(dst=self.dst,src=self.src, len=l)/TCP(dport=self.dport, seq=self.seq)
        return p

    def __str__(self):
        return self.src + ":" + str(self.dport)
