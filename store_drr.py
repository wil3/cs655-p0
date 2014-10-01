import simpy
import time

from store_super import QStore

class DRRStore(QStore):
    
    def __init__(self, env):
        super(DRRStore, self).__init__(env)
    
    def _do_get(self, event):
        if self.items:
            pkt = self.items.pop(0)
            pkt.set_depart_time(time.time())
            self._log.append(pkt)
            event.succeed(pkt)
