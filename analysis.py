
import time
import numpy as np
import matplotlib.pyplot as plt


class QMetrics:
    
    def __init__(self, data):
        self._data = data

    def print_data(self):

        #After the experiment as run this is the data that has been logged
        for src in self._data:
            pkts = self._data[src]
            for pkt in pkts:
                print str(pkts[pkt])
    
    def compute_total_tx(self, pkts):
        """Accumulate all the payloads"""
        accum=0
        for seq in pkts:
            accum = accum + pkts[seq].len
        return accum

    def get_first_arrived_packet(self, pkts):
        """
        Of all the packets the source sent
        get the first one sent, this may not be the same as the first sequence
        """
        earliest = 10000;#something big
        first_pkt =pkts[0] 
        for seq in pkts:
            pkt = pkts[seq]
            if pkt.get_arrive_time() < earliest:
                earliest = pkt.arrive_time
                first_pkt = pkt

        return first_pkt

    def compute_throughput(self, pkts):
        """ 
        Compute the throughput of the packets from a source by the sum of 
        all bits transmitted divided by the difference between the last 
        packet transmitted and arrival of first packet

        return throughput in bps
        """
        b=self.compute_total_tx(pkts)
        #First packet (seq=0) might actually be large and not be the first 
        #packet to arrive
        a=self.get_first_arrived_packet(pkts).get_arrive_time()
        seq_last=len(pkts)-1
        f=pkts[seq_last].tx_time

        return b/(f-a)

    def get_source_list(self):
        """
        Get an array of all the sources
        """
        sources = []
        for src in self._data:
            sources.append(src)
        return sources

    def get_source_throughputs(self):
        """
        Get an array of each sources total throughput

        return array in same order as source array
        """
        throughputs= []
        #src is the ip address
        for src in self._data:
            pkts = self._data[src]
            throughputs.append(self.compute_throughput(pkts))
        return throughputs

    def get_source_mean_latency(self,pkts):
        """
        Compute the average latency for source
        """
        accum=0
        for seq in pkts:
            pkt = pkts[seq]
            accum = accum + pkt.get_queue_delay()

        return accum / len(pkts)

    def get_source_latencies(self):
        
        delays= []
        #src is the ip address
        for src in self._data:
            pkts = self._data[src]
            delays.append(self.get_source_mean_latency(pkts))
        return delays

    def plot_rate(self):
        sources=self.get_source_list()
        rates=self.get_source_throughputs()
        print sources
        print rates
        plot("Source Throughput","Throughput (bps)", "Sources", sources, rates)

    def plot_latency(self):
        sources=self.get_source_list()
        latency = self.get_source_latencies()
        print latency
        plot("Source Latencies","Latency", "Sources", sources, latency)



class QAnalysis:

    def __init__(self):
        pass

    def plot(self, label, ylabel, xlabel, xticks, data):
        """
        label: the plot label
        ylabel: the y-axis label
        xticks: the labels for each tickmark of the x-axis
        data: a list of items of the form (label, avgresults)
        """

#TODO Figure out how we deal with running exp multiple times
        #data = []
        #for src in sample:
        #    data.append([src])
            
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(label)
      #  for (linelabel, avgresults) in data:
#TODO Still need to calculate these values
      # usermedians can be overriden...will be line use mean instead
      # conf_intervals
        plt.boxplot(data)
        plt.xticks(range(1, len(xticks)+1), xticks)
#        legendstrings.append(linelabel)
#    if len(data) > 1:
#        Plt.legend(legendstrings)
        plt.show()
