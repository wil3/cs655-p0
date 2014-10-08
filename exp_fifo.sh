#!/bin/bash
source virtualenv-1.9/ve_pa0/bin/activate
python main.py -x 10 -n 10000 -M 1 --fifo
deactivate
