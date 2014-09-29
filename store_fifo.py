
import simpy
import time

class QStore(simpy.Store):
    
    def __init__(self, env):
        super(QStore, self).__init__(env)
        self._log = []

    def get_log(self):
        return self._log

class FIFOStore(QStore):
    
    def __init__(self, env):
        super(FIFOStore, self).__init__(env)
    
    def _do_get(self, event):
        if self.items:
            pkt = self.items.pop(0)
            pkt.set_depart_time(time.time())
            self._log.append(pkt)
            event.succeed(pkt)

    def _do_put(self,event):
        event.item.set_arrive_time(time.time())
        super(QStore, self)._do_put(event)
