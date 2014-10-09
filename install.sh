#!/bin/bash

#Download virtualenv
curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.tar.gz
#Unpacked it
tar xvfz virtualenv-1.9.tar.gz
#cd virtualenv-1.9
#This creates the virtual environment named ve_pa0
python virtualenv-1.9/virtualenv.py --system-site-packages ve_pa0
#cd ve_pa0

#activate ve and now pip is available to install dependencies
source ve_pa0/bin/activate
#Install simpy
pip install simpy
#now run our code
#python <script to run>.py
#get out of ve
deactivate
