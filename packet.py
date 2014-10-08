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
        self.arrive_time = 0 #Arrives in the queue
        self.depart_time = 0 #time in which the packet is grabbed from the queue and begins tx
        self.tx_time = 0 #Time at which packet is fully tx

    def set_arrive_time(self, arrive_time):
        """Sets the time at which the packet arrives in the queue."""
        self.arrive_time = arrive_time

    def get_arrive_time(self):
        """Gets the time at which the packet arrives in the queue."""
        return self.arrive_time

    def set_depart_time(self, depart_time):
        """Sets the time at which the packet departs from the queue."""
        self.depart_time = depart_time

    def get_depart_time(self):
        """Gets the time at which the packet departs from the queue."""
        return self.depart_time
    
    def get_queue_delay(self):
        """
        Returns the amount of time (in seconds) that the packet spent in the
        queue.
        """
        if (self.depart_time != None) and (self.arrive_time != None):
            return self.depart_time - self.arrive_time
        return None

    def __str__(self):
        """
        Gives a text representation of the packet.
        """
        bps = 0
        delta = self.tx_time - self.arrive_time
        if delta > 0:
            print "Delta ", delta
            bps = self.len / (delta *1.0)
        return "%d\t%s -> %d(%d)\tdepart=%f\tarrive=%f\tq=%f\ttx=%f\td=%f\tbps=%f" % (self.seq, self.src, self._dport,self.len,self.depart_time, self.arrive_time, self.get_queue_delay(), self.tx_time, delta, bps)






