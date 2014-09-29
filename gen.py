try:
    from scapy import *
except:
    print "error import"
import random

MU_TELNET_SIZE = 512
MU_FTP_SIZE = 8192
SIGMA = 20 

print random.gauss(MU_TELNET_SIZE,20)
try:
    ftp = IP(dst="localhost")/TCP(dport=23)
    print ftp
except:
    print "error"
