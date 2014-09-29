#import logging
#logging.getLogger("scapy.loading").setLevel(logging.CRITICAL)
#from scapy import *
import random
"""

"""
PKT_LEN_SIGMA = 20
pkt_counter = 0

class Packet:
    def __init__(self, src, dst, len, seq, dport):
        self.src = src
        self.dst = dst
        self.len = len
        self.seq = seq
        self.dport = dport
        self.arrive_time = 0
        self.depart_time = 0

    def get_arrive_time(self):
        return self.arrive_time

    def set_arrive_time(self, time):
        self.arrive_time = time

    def get_depart_time(self):
        return self.depart_time

    def set_depart_time(self, time):
        self.depart_time = time
    
    def get_queue_delay(self):
        return self.depart_time - self.arrive_time

    def __str__(self):
        return self.src + ":" + str(self.dport) + " " + str(self.len)

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
            print "#", pkt_counter , " " , str(pkt)
            pkt_counter = pkt_counter + 1
            tx_delay = pkt.len/rate

            yield self.env.timeout(tx_delay) #This symbolizes the transmission delay
            yield self.store.put(pkt) #And the packet added to the queue
            seq = seq + 1
            
    def build_pkt(self,l, seq):
        p = Packet(self.src, self.dst, l, seq, self.dport)
        #l = random.gauss(mu_len,PKT_LEN_SIGMA)
      #  p = IP(dst=self.dst,src=self.src, len=l)/TCP(dport=self.dport, seq=self.seq)
        return p

    def __str__(self):
        return self.src + ":" + str(self.dport)
