class Packet:
    """Represents a packet"""
    
    def __init__(self, src, dst, length, seq, dport):
        """
        Initiates the packet with:
        src: source ip
        dst: destination ip
        length: packet size
        seq: ?
        dport: destination port
        """
        self.src = src
        self.dst = dst
        self.len = length
        self.seq = seq
        self._dport = dport
        self._arrive_time = 0
        self._depart_time = 0
        self.tx_time = 0 #Time at which packet is fully tx

    def set_arrive_time(self, arrive_time):
        """Sets the time at which the packet arrives in the queue."""
        self._arrive_time = arrive_time

    def get_arrive_time(self):
        """Gets the time at which the packet arrives in the queue."""
        return self._arrive_time

    def set_depart_time(self, depart_time):
        """Sets the time at which the packet departs from the queue."""
        self._depart_time = depart_time

    def get_depart_time(self):
        """Gets the time at which the packet departs from the queue."""
        return self._depart_time
    
    def get_queue_delay(self):
        """
        Returns the amount of time (in seconds) that the packet spent in the
        queue.
        """
        if (self._depart_time != None) and (self._arrive_time != None):
            return self._depart_time - self._arrive_time
        return None

    def __str__(self):
        """
        Gives a text representation of the packet.
        """
        return "%d\t%s(%d)\tq=%f\ttx=%f" % (self.seq, self.src, self.len, self.get_queue_delay(), self.tx_time)






