#Code to upload the configuration file created by createospf.py code to the router through ssh
try:
    import netmiko
    from netmiko import ConnectHandler
    import json
    import threading
    import os
    import csv
    from login_info import *
    from create_ospf import *
except:
    print('Please install required modules')

#Sending config files to routers
def conn(i,j):
        connect=netmiko.ConnectHandler(**j)
        connect.enable()
        connect.send_config_from_file(i)
        

def ospf(filename):
    #Loading sshinfo into a variable
    s=Parse_file(filename)
    print(s)

    #Creating a dictionary to send respective configurations
    routers={'R1_ospfconf.txt':s['R1'],'R2_ospfconf.txt':s['R2'],'R3_ospfconf.txt':s['R3'],'R4_ospfconf.txt':s['R4'],'R5_ospfconf.txt':s['R5'],'R6_ospfconf.txt':s['R6']}
    print(routers)


        
    #Threading
    thread=[]
    for i,j in routers.items():
        t1=threading.Thread(target=conn,args=(i,j))
        t1.start()
        thread.append(t1)
    
    for j in thread:
        j.join()

    print('DONE')

if __name__=='__main__':
    ospfconf_create()
    ospf('sshInfo-2.csv')
