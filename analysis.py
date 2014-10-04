
import time
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import math

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

    def plot(self, label, ylabel, xticks, data):
        """
        label: the plot label
        ylabel: the y-axis label
        xticks: the labels for each tickmark of the x-axis
        data: a list of items of the form (label, avgresults)
        """
        xlabel = "Sources"
#TODO Figure out how we deal with running exp multiple times
        #data = []
        #for src in sample:
        #    data.append([src])

        # setting up the plot:
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(label)
        xtickslocs = range(1, len(xticks)+1)
        plt.xticks(xtickslocs, xticks)
        # create the box plot:
        this_plot = plt.boxplot(data)
                                #notch=True,
                                #usermedians=means)
                                #conf_intervals=conf_intervals)
        means = [np.mean(dataset) for dataset in data]
        conf_intervals = [stats.bayes_mvs(dataset, alpha=.9)[0][1]
                          for dataset in data]
        conf_interval_lower = [ci[0] for ci in conf_intervals]
        conf_interval_upper = [ci[1] for ci in conf_intervals]
        # mark the means separately, since it does not make sense to use means
        # instead of medians in a box plot:
        plt.scatter(xtickslocs, means)
        # because we are not using the median, we mark our confidence intervals
        # separately also:
        plt.scatter(xtickslocs, conf_interval_lower, c='red')
        plt.scatter(xtickslocs, conf_interval_upper, c='red')
        # making sure the plot is correct:
##        displayed_means = [float(data_point.get_ydata()[0]) for data_point in
##                           this_plot["medians"]]
##        for (desired_mean, displayed_mean) in zip(means, displayed_means):
##            assert desired_mean == displayed_mean
        # displaying the plot:
        plt.show()
