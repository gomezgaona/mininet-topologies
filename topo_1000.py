#!/usr/bin/python

import os
import subprocess
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI

def start_mininet_hosts(num_hosts, buffer_size):
    if(num_hosts > 254):
        print("You are trying to add more than 254 senders and receivers")
        return
    net = Mininet(topo=None, build=False, ipBase='10.0.0.0/24')

    # Create switches
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')
    print("Creating switches")
    net.addLink(s1, s3)
    net.addLink(s2, s3)
    # Start hosts and connect them to the switch
    for i in range(1, int(num_hosts/2) + 1):
        h = net.addHost(f'h{i}', ip=f'10.0.0.{i}/24')
        net.addLink(h, s1)
    
    for i in range(int(num_hosts/2) + 1, num_hosts):
        h = net.addHost(f'h{i}', ip=f'10.0.0.{i}/24')
        net.addLink(h, s2)
 
    for i in range(1, num_hosts + 1):    
        h.cmd('sysctl -w net.ipv4.tcp_wmem="{} {} {}"'.format(buffer_size, buffer_size, buffer_size))
        h.cmd('sysctl -w net.ipv4.tcp_rmem="{} {} {}"'.format(buffer_size, buffer_size, buffer_size))
    
    for i in range(1, num_hosts + 1):
         h.cmd('ip route add 20.0.0.0/24 via 10.0.0.0.254')
    print(f"Creating hosts, setting TCP send and receive buffers to {buffer_size}, and connecting hosts to the switches")
    
    
    # Start the network
    net.start()
    print("Starting the network")
    
    # Open the Mininet CLI
    net.interact()
    
    # Clean up after the network has been stopped
    net.stop()

# Enter the number of hosts
num_hosts = 100
TCP_buffer_size = "4096 1000000 200000000"

start_mininet_hosts(num_hosts, TCP_buffer_size)


