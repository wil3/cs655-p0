import simpy
import time

from store_super import QStore
#Number of bytes that a flow is allows to transmit when it is its turn
DEFICIT_COUNTER = 100
class DRRStore(QStore):
    
    def __init__(self, env):
        super(DRRStore, self).__init__(env)
    
    def _do_get(self, event):
        if self.items:
            pkt = self.items.pop(0)
            pkt.set_depart_time(time.time())
            self._log.append(pkt)
            event.succeed(pkt)

    def _do_put(self, event):
        pkt = event.item
        pkt.set_arrive_time(time.time())
