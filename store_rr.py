import simpy
import time

from store_super import QStore
from packet import Packet

class RRStore(QStore):
    """Round Robin queue"""
    
    def __init__(self, env):
        """
        Initializes the Round Robin queue.
        This queue is actually composed of a `queue of queues'.
        """
        super(RRStore, self).__init__(env)
        self.__queues = {}
        self.__queue_tracker = []

    def __get_next_queue(self):
        """Returns the next key (sourceip, destinationip) and the associated
        queue  in the round robin"""
        (key, queue) = (None, None)
        if len(self.__queue_tracker) > 0:
            key = self.__queue_tracker.pop(0)
            self.__queue_tracker.append(key)
            queue = self.__queues[key]
        return (key, queue)
            
        

    def __add_to_queue(self, key, val):
        """adds the given packet to the queue corresponding to the given key,
        which should be a (sourceip, destinationip) pair"""
        if not (key in self.__queues):
            self.__queues[key] = []
            self.__queue_tracker.append(key)
        self.__queues[key].append(val)

    def __get_packet(self):
        """returns the next packet, at the same time updating the order in
        which the queues are to be checked"""
        checked_keys = [] # keeps track of the queues checked during this
                          # operation
        packet = None
        key = None
        while ((not packet) and
               (not (key in checked_keys)) and
               len(checked_keys) < len(self.__queue_tracker)):
            (key, queue) = self.__get_next_queue()
            checked_keys.append(key)
            if len(self.__queues[key]) > 0:
                packet = self.__queues[key].pop(0)
        return packet

    def _do_put(self, event):
        """Adds a packet"""
        super(RRStore, self)._do_put(event)
        if sum([len(queue) for queue in self.__queues.values()]) < self._capacity:
            key = (event.item.src, event.item.dst)
            val = event.item
            self.__add_to_queue(key, val)
            event.succeed()
    
    def _do_get(self, event):
        """Gets the next packet"""
        item = None
        packet = self.__get_packet()
        if packet:
            packet.set_depart_time(time.time())
            self._log.append(packet)
            event.succeed(packet)

def test_rrstore():
    """
    Test the round robin queue.
    """
    env = simpy.Environment()
    log = [] # keeps track if returned packets
    
    def put(env, store, item):
        print "adding %s" % str(item)
        yield store.put(item)

    def get(env, store, log):
        item = yield store.get()
        print "getting %s" % str(item)
        log.append(item)
    
    thisstore = RRStore(env)
    packet1 = Packet("src1ip", "dstip", 100, None, None)
    packet2 = Packet("src1ip", "dstip", 100, None, None)
    packet3 = Packet("src2ip", "dstip", 100, None, None)
    env.process(put(env, thisstore, packet1))
    env.process(put(env, thisstore, packet2))
    env.process(put(env, thisstore, packet3))
    env.process(get(env, thisstore, log))
    env.process(get(env, thisstore, log))
    env.process(get(env, thisstore, log))
    env.run()
    print "Store yeilds packets in this order: %s" % (
       ", ".join([str(pkt) for pkt in log]))
    [yieldedpacket1, yieldedpacket2, yieldedpacket3] = log
    assert yieldedpacket1 == packet1
    assert yieldedpacket2 == packet3
    assert yieldedpacket3 == packet2

if __name__ == "__main__":
    test_rrstore()

