#!/usr/bin/env python3

# Importing required modules
try:
	import netmiko
	from netmiko import ConnectHandler
	import json
	import prettytable
	from prettytable import PrettyTable
	from login_info import *
except:
	print('Install required modules')

# Function to get IP address on each interface of all routers
def get_ips(r):
	interfaces={}
	conn=netmiko.ConnectHandler(**r)
	conn.enable()
	out=conn.send_command('sh ip int brief')
	out=out.split('\n')
	for i in range(len(out)):
		a=out[i].split()
		if a[4]=='up':
			interfaces[a[0]]=a[1]
	
	return interfaces


# Function to get BGP information
def get_bgp(r):
	conn=netmiko.ConnectHandler(**r)
	conn.enable()
	out=conn.send_command('sh ip bgp neighbors')
	o=out.split('\n')
	
	return o[0].split()[3][:-1],o[0].split()[6][:-1],o[2].split()[3][:-1]

# Function to get OSPF information 
def get_ospf(r):
	a=[]
	conn=netmiko.ConnectHandler(**r)
	conn.enable()
	out=conn.send_command('sh ip ospf neighbor')
	o=out.split('\n')
	for i in o[2:]:
		a.append([i.split()[0],i.split()[1],i.split()[2],i.split()[-1]])
		
	return a

# Function to get running configurations of a router
def get_running_config(R,r):
	conn=netmiko.ConnectHandler(**r)
	conn.enable()
	out=conn.send_command('sh run')
	filename=R+'_running_config.txt'
	f=open(filename,'w')
	f.write(out)
	f.close()
	print('Running configs saved to file '+filename)

# Main Function
def main(ch):
	try:
		'''with open ('sshinfo.txt') as f:
			data1=json.load(f)'''
		data1=Parse_file('sshInfo-2.csv')
		print(data1)
	except:
		print('ssh file does not exist!')
	'''try:
		with open ('sshinfo.json') as f:
			data2=json.load(f)
	except:
		print('ssh file does not exist!')'''

	
	if ch=='1':
		z=PrettyTable()
		z.field_names=['Router','Interface','IP']
		for k,v in data1.items():
			intf=get_ips(v)
			for k2,v2 in intf.items():
				z.add_row([k,k2,v2])
		
		filename='InterfacesIP.txt'
		f=open(filename,'w')
		f.write(str(z))
		f.close()	
		print('Configurations are stored in '+filename)	
	
	elif ch=='2':
		y=PrettyTable()
		y.field_names=['Router','Neighbor IP','Remote AS','State']
		for i,j in data1.items():
			try:
				nip,ras,stt=get_bgp(j)
				y.add_row([i,nip,ras,stt])
			except:
				continue

		filename='BGPinfo.txt'
		f=open(filename,'w')
		f.write(str(y))
		f.close()
		print('Configurations are stored in '+filename)

	elif ch=='3':
		l1={}
		x=PrettyTable()
		x.field_names=['Router','Neighbor IP','Process ID','State', 'Interface']
		for i,j in data1.items():
			l1[i]=get_ospf(j)
			for k in range(len(l1[i])): 
				x.add_row([i,l1[i][k][0],l1[i][k][1],l1[i][k][2],l1[i][k][3]])
		
		filename='OSPFinfo.txt'
		f=open(filename,'w')
		f.write(str(x))
		f.close()
		print('Configurations are stored in '+filename)

	elif ch=='4':
		for k,v in data1.items():
			get_running_config(k,v)

	else:
		print('Bad choice! Exiting...')
		exit()

if __name__=='__main__':
	main('1')
	main('2')
	main('3')
	main('4')
