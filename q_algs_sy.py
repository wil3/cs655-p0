import simpy
import logging
logging.basicConfig(level=logging.INFO) #filename='router.log', 
class Packet:
    """A class representing a single packet"""
    def __init__(self, packetid, sourceip=None, destip=None, size=0):
        self.id = packetid
        self.sourceip = sourceip
        self.destip = destip
        self.size = size

    def get_sendingtime(self):
        return self.size + 3 # what should this actually be?

    def __str__(self):
        return "".join([str(self.id), ":", str(self.sourceip),
                        "->", str(self.destip)])

class Queue:
    """A class representing a queue of packets"""
    def __init__(self, queue=[]):
        self._queue = queue

    def push(self, packet):
        """adds a packet to the queue"""
        self._queue.append(packet)

    def pop(self):
        """gets a packet from the queue, and removes that packet"""
        return self._queue.pop()

    def size(self):
        """returns the number of packets in the queue"""
        return len(self._queue)

    def __str__(self):
        "|".join([str(packet) for packet in self._queue])
        
class Router:
    """A class representing a router"""
    def __init__(self, env, queue=Queue()):
        """
        env: the simpy environment
        queue: the router queue, initially empty by default
        """
        logging.info("created a router")
        self.env = env
        self.queue = queue
        
    def receive(self, packet):
        """The router receives a packet"""
        self.queue.push(packet)
        logging.info("%s: received packet %s" % (self.env.now, packet))

    def send(self):
        """The router sends a packet"""
        if self.queue.size() > 0:
            packet = self.queue.pop()
            logging.info("%s: sending packet %s" % (self.env.now, packet))
            yield self.env.timeout(packet.get_sendingtime())

    def run(self, store):
        while True:
            # queue any incoming packets:
            packet = yield store.get()
            self.receive(packet)
            # send next available packet
            self.send() # TODO: this doesn't seem to be getting called
        
class PacketSource: #TODO: make this more interesting
    """A class representing a packet source"""
    def __init__(self, pmaketime, psize): 
        """
        pmaketime: the mean time it takes to make a packet
        psize: the size of every created packet
        """
        logging.info("created a packetsource")
        self.psize = psize
        self.pmaketime = pmaketime

        self.currentid = 0
        
    def make(self):
        """makes a packet and gives it to the router"""
        packet = Packet(packetid=self.currentid, size=self.psize)
        logging.info("%s: making packet %s" % (env.now, packet))
        self.currentid += 1
        return packet

    def run(self, env, store, numpackets):
        for packetnum in xrange(numpackets):
            packet = self.make()
            yield env.timeout(self.pmaketime)
            yield store.put(packet)

env = simpy.Environment()

store = simpy.Store(env)

packetsource = PacketSource(10, 10)

router = Router(env)

numpackets = 10

env.process(packetsource.run(env, store, numpackets))

env.process(router.run(store))

env.run(until=100)
