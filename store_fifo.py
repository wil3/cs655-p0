
import simpy
import time

from store_super import QStore
from packet import Packet

class FIFOStore(QStore):
    
    def __init__(self, env):
        super(FIFOStore, self).__init__(env)
    
    def _do_get(self, event):
        if self.items:
            pkt = self.items.pop(0)
            pkt.set_depart_time(time.time())
            self._record(pkt)
            event.succeed(pkt)
            print self._print_q_out()

    def _do_put(self,event):
        event.item.set_arrive_time(time.time())
        super(QStore, self)._do_put(event)
        print self._print_q_in()

    def print_q(self, border):
        return border + "\n" + self._get_queue_str(self.items) + "\n" + border + "\n"

    def __str__(self):
        bottom = "-------------\n"
        return bottom + self._get_queue_str(self.items) + "\n" + bottom

def test_fifostore():
    """
    Test the first in first out queue.
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
    
    thisstore = FIFOStore(env)
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
    assert yieldedpacket2 == packet2
    assert yieldedpacket3 == packet3

if __name__ == "__main__":
    test_fifostore()
