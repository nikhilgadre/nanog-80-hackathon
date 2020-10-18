from netmiko import ConnectHandler
from threading import Thread
from napalm import get_network_driver
import json
import re
import sys
import os
import pandas as pd
from prettytable import PrettyTable


def fetch_information(ssh_details):
    con = ConnectHandler(**ssh_details)
    cmd0 = con.send_command('ping 2.2.2.2 source lo0 ')
    cmd1 = con.send_command('sh crypto isakmp sa')
    cmd2 = con.send_command('sh crypto ipsec sa')
    cmd3 = con.send_command('ping 2001::3 source lo1')
    return cmd0, cmd1, cmd2, cmd3

def vpn_conf():
    filename = "sshInfo-2.csv"
    f = open(filename)
    rf = pd.read_csv(f)
    ssh_info = rf.to_dict(orient='records')
    print(*ssh_info)
    file = 'vpn.txt'
    optional_args = {'dest_file_system': 'nvram:'}
    optional_args['dest_file_system'] = 'nvram:'
    driver = get_network_driver('ios')
    ip = ssh_info[-1]['ip']
    uname = ssh_info[-1]['username']
    pwd = ssh_info[-1]['password']
    print(ip, uname, pwd)
    print("\nConfiguring VPNuser")
    dev = driver(ip, uname, pwd, optional_args={'global_delay_factor': 2})
    dev.open()
    dev.load_merge_candidate(filename=file)
    diff = dev.compare_config()
    if len(diff) > 0:
        print('hello')
        dev.commit_config()
        print('VPN and 6to4 tunnel are configured')
    else:
        print('No configurations')
    dev.close()
    ssh_info = {
    'device_type': 'cisco_ios',
    'username': 'test',
    'password': 'test',
    'ip': '192.168.100.99',
    }
    x, y, z, w = fetch_information(ssh_info)

    print("\n------------------- Ping from VPNuser loopback0 to R3 loopback0 -------------------\n")
    print(x)
    print("\n-------------------Show security associations for VPN -------------------\n")
    print(y)
    print("\n------------------- Show statistics -------------------\n")
    # print(z)
    table = PrettyTable(['Local tunnel ep', 'Remote tunnel ep', 'No. of encrypted pkts', 'No. of decrypted pkts', 'Tunnel status'])
    a = re.findall(r'(?<=local crypto endpt.: )(\d+\.\d+\.\d+\.\d+)', z)
    b = re.findall(r'(?<=remote crypto endpt.: )(\d+\.\d+\.\d+\.\d+)', z)
    c = re.findall(r'(?<=#pkts encrypt: )(\d+)', z)
    d = re.findall(r'(?<=#pkts decrypt: )(\d+)', z)
    e = re.findall(r'(?<=Status: )(\w+)', z)
    # print(a,b,c,d,e[0])
    table.add_row([a[0], b[0], c[0], d[0], e[0]])
    print(table)
    print("\n------------------- Ping from IPv6 address at VPNuser to IPv6 address at R3 -------------------\n")
    print(w)
    return table,w

#vpn_conf()
