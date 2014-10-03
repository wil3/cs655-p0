
import time

import numpy as np
import matplotlib.pyplot as plt

RTTMSIZES = [1, 100, 200, 400, 800, 1000]
TPUTMSIZES = [1000, 2000, 4000, 8000, 16000, 32000]


class QAnalysis:
    
    def __init__(self, data):
        self._data = data

    def print_data(self):

        #After the experiment as run this is the data that has been logged
        for src in self._data:
            pkts = self._data[src]
            for pkt in pkts:
                print str(pkts[pkt])

def plot(label, ylabel, xticks, avgresultslist):
    """
    label: the plot label
    ylabel: the y-axis label
    xticks: the labels for each tickmark of the x-axis
    avgresultslist: a list of items of the form (label, avgresults)
    """
    fig, ax = plt.subplots()
    plt.xlabel("message size (in bytes)")
    plt.ylabel(ylabel)
    plt.title(label)
    ax.set_xticklabels(xticks)
    legendstrings = []
    for (linelabel, avgresults) in avgresultslist:
        plt.plot(avgresults, 'o-')
        legendstrings.append(linelabel)
    if len(avgresultslist) > 1:
        plt.legend(legendstrings)
    plt.show()

def perform_rtt_tests(hostname, portnumber, numprobes, sdelays=None):
    """A script that performs all of the tests for rtt."""
    mtype = 'rtt'
    avgresultslist = []
    if sdelays == None:
        sdelays = [0]
    for sdelay in sdelays:
        avgresults = []
        for msize in RTTMSIZES:
            client = Client(hostname, portnumber)
            results = client.RUN(mtype, numprobes, msize, sdelay)
            avg = float(sum(results))/float(len(results))
            avgresults.append(avg)
        linelabel = 'delay=%s, numprobes=%s' % (str(sdelay), str(numprobes))
        avgresultslist.append((linelabel, avgresults))
    plot(mtype, mtype, RTTMSIZES, avgresultslist)

def perform_tput_tests(hostname, portnumber, numprobes, sdelays=None):
    """A script that performs all of the tests for tput."""
    mtype = 'tput'
    avgresultslist = []
    if sdelays == None:
        sdelays = [0]
    for sdelay in sdelays:
        avgresults = []
        for msize in TPUTMSIZES:
            client = Client(hostname, portnumber)
            results = client.RUN(mtype, numprobes, msize, sdelay)
            avg = float(sum(results))/float(len(results))
            avgresults.append(avg)
        linelabel = 'delay=%s, numprobes=%s' % (str(sdelay), str(numprobes))
        avgresultslist.append((linelabel, avgresults))
    plot(mtype, mtype, TPUTMSIZES, avgresultslist)
