import simpy


#This specifices how many packets we can receive at a time
RECQ_SIZE = 5

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
        print env.now, '>> ip=', pkt.get_ip()
        yield env.timeout(3) #this is the tx time l/bps
        print_queue(store.items)



env = simpy.Environment()
#The default store is already FIFO so we need to look
#into how to create our stores so when a get is called
#it uses the other algorithms
store = simpy.Store(env, capacity=RECQ_SIZE)

env.process(pkt_producer(env,store))

#init number of pkts
env.process(router_tx(env, store))

env.run(until=10)
