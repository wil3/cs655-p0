import logging
logging.getLogger("scapy.loading").setLevel(logging.CRITICAL)

import simpy

from source import *
#from scapy import *
#This specifices how many packets we can receive at a time
RECQ_SIZE = 5
FTP_PORT = 20
FTP_LENGTH = 8192 #bits
TELENET_PORT = 23
TELENET_LENGTH = 512 #bits
ROUTER_IP = "192.168.1.1"
class Packet:
    def __init__(self, ip=0):
        self.ip = ip
    def get_ip(self):
        return self.ip
    def set_ip(self,ip):
        self.ip = ip

def print_queue(q):
    pkts = ""
    for pkt in q:
        pkts += pkt.get_ip() + "|"
    print pkts

def pkt_producer(env, store):
    for i in range(10):
        yield env.timeout(1) # What is the rate in which they are transmitted?
        yield store.put(Packet(str(i)))
        print env.now, 'ip=', i, '>>'

def router_tx(env, store):
    while True:
        #print 'Any packets at t=', env.now, '?'
        pkt = yield store.get() #Store is FIFO, when this is called the packet is consumed because the store is a generator
        #pkt = IP(data)
        print env.now, '>> ip=', pkt.src +":"+str(pkt.dport) + "[" + str(pkt.len) + "]"
        yield env.timeout(3) #this is the tx time l/bps
        #print_queue(store.items)


SCALE= 5;
env = simpy.Environment()
#The default store is already FIFO so we need to look
#into how to create our stores so when a get is called
#it uses the other algorithms
store = simpy.Store(env, capacity=RECQ_SIZE)

BASE_IP = "192.168.1"
#ENV.PROCEss(pkt_producer(env,store))
def create_sources(count, start_ip, dport, rate, mu_len, variate):
    for i in range(count):
        ip = BASE_IP + "." + str(start_ip + i)
        s = TrafficSource(env, store, dport, ip, ROUTER_IP)
        print "Creating ", str(s)
        env.process(s.tx(rate, mu_len, variate))


#create ftp sources
create_sources(6, 100, FTP_PORT, 1, FTP_LENGTH, True)
#create telnet sources
create_sources(4, 107, TELENET_PORT, 1, TELENET_LENGTH, True)
#create rouge
create_sources(1, 112, 6666, 0.5, 5000, False)

#init number of pkts
env.process(router_tx(env, store))

env.run(until=1000)


