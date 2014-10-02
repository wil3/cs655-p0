import logging
import argparse
import simpy
from store_fifo import FIFOStore
from store_rr import RRStore
from store_drr import DRRStore
from source import *
#from scapy import *
#This specifices how many packets we can receive at a time
BASE_IP = "192.168.1"
FTP_PORT = 20
FTP_LENGTH = 8192 #bits
TELENET_PORT = 23
TELENET_LENGTH = 512 #bits
ROUTER_IP = "192.168.1.1"

class Router:
    def __init__(self, env, store):
        self.env = env
        self.store = store

    def tx(self):
        while True:
#            print str(self.env.now)
#            print  str(self.store)
            #print 'Any packets at t=', env.now, '?'
            pkt = yield self.store.get() #Store is FIFO, when this is called the packet is consumed because the store is a generator
#            print str(self.env.now)
#            print str(self.store)
            #pkt = IP(data)
            print '<<', pkt.src + "(" + str(pkt.len) + ")"
            yield self.env.timeout(pkt.len) #this is the tx time l/bps
            #print self.env.now, '\t\t', str(pkt) , ">>"





def create_sources(env, store, count, start_ip, dport, rate, mu_len, variate):
    for i in range(count):
        ip = BASE_IP + "." + str(start_ip + i)
        s = TrafficSource(env, store, dport, ip, ROUTER_IP)
        print "Creating ", str(s)
        env.process(s.tx(rate, mu_len, variate))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Test various queuing algorithms')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--fifo', action='store_true')
    group.add_argument('--rr', action='store_true')
    group.add_argument('--drr', action='store_true')
    args = parser.parse_args()

    env = simpy.Environment()
    store = None
    if args.fifo:
        store = FIFOStore(env) #simpy.Store(env, capacity=RECQ_SIZE)
    elif args.rr:
        store = RRStore(env)
    elif args.drr: #drr
        store = DRRStore(env)
    else:
        assert False, "not given a router type argument"

#create ftp sources
    create_sources(env, store, 2, 100, FTP_PORT, .1, FTP_LENGTH, True)
#create telnet sources
    create_sources(env, store, 2, 107, TELENET_PORT, 1, TELENET_LENGTH, True)
    #Create rouge
    #create_sources(env, store, 1, 112, 6666, 0.5, 5000, False)

    router = Router(env,store)
    env.process(router.tx())

    env.run()

    
    #After the experiment as run this is the data that has been logged
    for pkt in store.get_log():
        if pkt:
            print str(pkt) , str(pkt.get_queue_delay())



