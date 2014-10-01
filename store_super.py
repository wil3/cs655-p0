
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
        self._log = []

    def _do_put(self, event):
        event.item.set_arrive_time(time.time())
        #super(QStore, self)._do_put(event)

    def get_log(self):
        """Returns the log."""
        return self._log
