import simpy
import time

from store_rr import RRStore
from packet import Packet

class DRRStore(RRStore):
    """Deficit Round Robin queue"""
    
    def __init__(self, env, deficitcounter=100):
        """
        Initializes the Deficit Round Robin queue.
        Like the Round Robin queue, this queue is composed of a `queue of
        queues'.
        deficitcounter: number of bytes that a flow is allows to transmit when it is its
        turn
        """
        super(DRRStore, self).__init__(env)
        self.__deficits = {}
        self.__deficitcounter = deficitcounter

    def _add_new_queue(self, key):
        """adds a queue for a new (sourceip, destinationip) key ASSUMING it is
        not already stored.
        Note that the assumption is not checked: this method should be sued with
        care.
        """
        super(DRRStore, self)._add_new_queue(key)
        self.__deficits[key] = 0        
    
    def _get_packet(self):
        """returns the next packet, at the same time updating the order in
        which the queues are to be checked"""
        packet = None
        key = None
        if sum([len(queue) for queue in self._queues.values()]) > 0:
            # if there are any packets in the queue
            while not packet:
                (key, queue) = self._get_next_queue()
                if len(self._queues[key]) > 0:
                    consideredpacket = self._queues[key][0]
                    self.__deficits[key] += self.__deficitcounter
                    if consideredpacket.len <= self.__deficits[key]:
                        self.__deficits[key] -= consideredpacket.len
                        packet = self._queues[key].pop(0)
        return packet

def test_drrstore():
    """
    Test the deficit round robin queue.
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
    
    thisstore = DRRStore(env)
    packet1 = Packet("src1ip", "dstip", 1000, None, None)
    packet2 = Packet("src1ip", "dstip", 100, None, None)
    packet3 = Packet("src2ip", "dstip", 100, None, None)
    env.process(put(env, thisstore, packet1))
    env.process(put(env, thisstore, packet2))
    env.process(put(env, thisstore, packet3))
    for timestep in xrange(20):
        env.process(get(env, thisstore, log))
    env.run()
    print "Store yeilds packets in this order: %s" % (
       ", ".join([str(pkt) for pkt in log]))
    [yieldedpacket1, yieldedpacket2, yieldedpacket3] = log
    assert yieldedpacket1 == packet3
    assert yieldedpacket2 == packet1
    assert yieldedpacket3 == packet2

if __name__ == "__main__":
    test_drrstore()
