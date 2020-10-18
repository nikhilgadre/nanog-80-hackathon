#!/usr/bin/env python3

#Importing all the required modules
try:	
	import os.path
	import netmiko
	from netmiko import ConnectHandler
	import json
	import threading
	import time
	import os
	import csv
	from login_info import *
	from create_bgp import *
except:
	print('Install required modules and try again.')

# This fuctions takes the router login information and files to be configured as input parameters
# and pushes the configurations in the router.
def conn(i,j):
		connect=netmiko.ConnectHandler(**j)
		connect.enable()
		connect.send_config_from_file(i)

# The main function where both the functions are called and
# threading is used to simultaneously push the configs to the routers.
def bgp(filename):
	s=Parse_file(filename)
	#print(s)

	routers={'R1_bgpconf.txt':s['R1'],'R2_bgpconf.txt':s['R2']}
	print(routers)

	thread=[]
	for i,j in routers.items():
		t1=threading.Thread(target=conn,args=(i,j))
		t1.start()
		thread.append(t1)

	for j in thread:
		j.join()

	print('DONE')

if __name__=='__main__':
	bgpconf_create()
	bgp('sshInfo-2.csv')
