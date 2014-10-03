
import simpy
import time

class QStore(simpy.Store):
    """
    Subclasses the simpy Store class for our needs.
    Should be further subclassed by a store implementing a specific queuing
    protocol.
    """
    
    def __init__(self, env):
        super(QStore, self).__init__(env)
        self._log = {}

    def _do_put(self, event):
        event.item.set_arrive_time(time.time())
        #super(QStore, self)._do_put(event)
    
    def _record(self, pkt):
        if not (pkt.src in self._log):
            self._log[pkt.src] = {}
        self._log[pkt.src][pkt.seq] = pkt

    def get_log(self):
        """Returns the log."""
        return self._log

    def _get_queue_str(self,q):
        pkts = ""
        for pkt in q:
            pkts += str(pkt.len) + "|"
        return pkts


    def _print_q_out(self):
        border = "<<----------"
        return self.print_q(border)

    def _print_q_in(self):
        border = "----------<<"
        return self.print_q(border)




