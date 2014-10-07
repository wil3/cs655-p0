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
        self._queues = {}
        self._queue_sizes = {}
        self._queue_tracker = []


    def _get_next_queue(self):
        """returns the next key (sourceip, destinationip) and the associated
        queue  in the round robin"""
        (key, queue) = (None, None)
        if len(self._queue_tracker) > 0:
            key = self._queue_tracker.pop(0)
            self._queue_tracker.append(key)
            queue = self._queues[key]
        return (key, queue)

    def _add_new_queue(self, key):
        """adds a queue for a new (sourceip, destinationip) key ASSUMING it is
        not already stored.
        Note that the assumption is not checked: this method should be sued with
        care.
        """
        self._queues[key] = []
        self._queue_sizes[key] = 0
        self._queue_tracker.append(key)

    def _add_to_queue(self, key, val):
        """adds the given packet to the queue corresponding to the given key,
        which should be a (sourceip, destinationip) pair"""
        if not (key in self._queues):
            self._add_new_queue(key)
        self._queues[key].append(val)
        self._queue_sizes[key] += val.len
        self._bufferoccupancy += val.len
        # if the buffer overflows:
        while self._bufferoccupancy > self._buffersize:
            inverse = [
                (tempkey, tempval) for tempval, tempkey
                in self._queue_sizes.items()]
            tempkey = max(inverse)[1]
            #print self._queues
            dropped_packet = self._queues[tempkey].pop(-1)
            self._queue_sizes[tempkey] -= dropped_packet.len
            self._bufferoccupancy -= dropped_packet.len

    def _get_packet(self):
        """returns the next packet, at the same time updating the order in
        which the queues are to be checked"""
        checked_keys = [] # keeps track of the queues checked during this
                          # operation
        packet = None
        key = None
        while ((not packet) and
               (not (key in checked_keys)) and
               len(checked_keys) < len(self._queue_tracker)):
            (key, queue) = self._get_next_queue()
            checked_keys.append(key)
            if len(self._queues[key]) > 0:
                packet = self._queues[key].pop(0)
        if packet:
            self._queue_sizes[key] -= packet.len
            self._bufferoccupancy -= packet.len
        return packet

    def _do_put(self, event):
        """Adds a packet"""
        if sum([len(queue) for queue in self._queues.values()]) < self._capacity:
            super(RRStore, self)._do_put(event)
            key = (event.item.src, event.item.dst)
            val = event.item
            self._add_to_queue(key, val)
            event.succeed()
            self.logger.debug(self._print_q_in())
    


    def _do_get(self, event):
        """Gets the next packet"""
        item = None
        packet = self._get_packet()
        if packet:
            packet.set_depart_time(time.time())
            self._record(packet)
            event.succeed(packet)
            self.logger.debug(self._print_q_out())


    def print_q(self, border):
        dmp = []
        if self._queues:
            for q in self._queues:
                dmp.append(str(q[0]) + "\t" + self.get_queue_str(self._queues[q]))

        return border + "\n".join(dmp) + "\n" + border

    def get_queue_str(self,queue):
        """Returns a string representation of the queue contents"""
        return "|".join([str(pkt.len) for pkt in queue])

    def __str__(self):
        dmp = []
        if self._queues:
            for q in self._queues:
                dmp.append(q[0] + "\t" + get_queue_str(self._queues[q]))

        bnd = "-------------\n"
        return bnd + "\n".join(dmp) + "\n" + bnd


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

