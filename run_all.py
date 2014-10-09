#import os
import main as q

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

ms = drange(0.4, 2.0, 0.2)
x = 5
n = 100000
algs = ['fifo', 'rr', 'drr']

for m in ms:

    for alg in algs:
        q.main(m, x, n, alg, True) 
#os.system(cmd)
