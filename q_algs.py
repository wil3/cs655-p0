import logging
import argparse
import simpy
import time
from store_fifo import FIFOStore
from store_rr import RRStore
from store_drr import DRRStore
from source import *
from analysis import *

#from scapy import *
#This specifices how many packets we can receive at a time
START_IP = 100
BASE_IP = "192.168.1."
FTP_PORT = 20
FTP_LENGTH = 8192 #bits
FTP_SOURCES = 2
TELENET_PORT = 23
TELENET_LENGTH = 512 #bits
TELENET_SOURCES = 2
ROUGE_SOURCES = 0 
ROUTER_IP = "192.168.1.1"
PKT_CREATE_MAX = 10
PKT_COUNTER = 0




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
            print '<<', str(pkt.src) + "(" + str(pkt.len) + ")"
            yield self.env.timeout(pkt.len) #this is the tx time l/bps
            
            #TODO Is this going to work for all algs?
            #self.store._log[pkt.src][pkt.seq].tx_time = time.time()
            pkt.tx_time = time.time()





def get_total_number_sources():
    return [FTP_SOURCES,TELENET_SOURCES,ROUGE_SOURCES]

def convert_to_real_name(index, port):
    return BASE_IP + str(START_IP + index) + "(" + str(port) + ")"

def get_real_source_list():
    sources = []
    last_ip =0
    k=0
    for i in get_total_number_sources():
        dport = '?'
        if k == 0:
            dport = str(FTP_PORT)
        elif k == 1:
            dport = str(TELENET_PORT)

        for j in range(i):
            sources.append(BASE_IP + str(START_IP + last_ip) + "(" + dport + ")") 
            last_ip = last_ip + 1
        k = k + 1

    return sources

def create_sources(env, store, count, start_ip, dport, rate, mu_len, variate, pool):
    for i in range(count):
#        ip = BASE_IP + "." + str(start_ip + i)
        ip = start_ip + i
        s = TrafficSource(env, store, dport, ip, ROUTER_IP, pool)
        print "Creating ", str(s)
        env.process(s.tx(rate, mu_len, variate))

def run(args):
    """
    Return tuple of latencies and throughputs
    """
    env = simpy.Environment()
    pkt_pool = simpy.Container(env, init=PKT_CREATE_MAX, capacity=PKT_CREATE_MAX)
    store = None
    if args.fifo:
        store = FIFOStore(env) #simpy.Store(env, capacity=RECQ_SIZE)
    elif args.rr:
        store = RRStore(env)
    elif args.drr: #drr
        store = DRRStore(env)
    else:
        assert False, "not given a queue algorithm  type argument"
#TODO mofidy these values
    #create ftp sources
    create_sources(env, store, FTP_SOURCES, 0, FTP_PORT, .1, FTP_LENGTH, True, pkt_pool)
    #create telnet sources
    create_sources(env, store, TELENET_SOURCES, FTP_SOURCES, TELENET_PORT, 1, TELENET_LENGTH, True, pkt_pool)
    #Create rouge
    #create_sources(env, store, 1, 112, 6666, 0.5, 5000, False)

    router = Router(env,store)
    env.process(router.tx())

    env.run()
    
    an = QMetrics(store.get_log())
    an.print_data()
    #The order of the data matches the source list so it needs to be returned
    #as well
    return (an.get_source_list(), an.get_source_latencies(), an.get_source_throughputs())









if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Test various queuing algorithms')
    parser.add_argument('-M', metavar='M', required=True, type=int, help='load')
    parser.add_argument('-x', metavar='x', type=int, help='Number of experiements to run')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--fifo', action='store_true')
    group.add_argument('--rr', action='store_true')
    group.add_argument('--drr', action='store_true')

    args = parser.parse_args()

    l = [None]*sum(get_total_number_sources())
    t = [None]*sum(get_total_number_sources())
    for i in range(args.x):
        (srcs, delay, tput) = run(args)
        sources = srcs
        print srcs
        print delay
        print tput
        
        for s in srcs:
            if l[s] == None:
                l[s] = [delay[s]]
                t[s] = [tput[s]]
            else:
                l[s].append(delay[s])
                t[s].append(tput[s])
    print l
    print t
    sources = get_real_source_list()
    print sources
    an = QAnalysis()
    an.plot("Source Throughput","Throughput (bps)", sources, t)
    an.plot("Source Latencies","Latency", sources, l)
#    an.print_data()
#    an.plot_rate()
#    AN.PLOt_latency()
    
