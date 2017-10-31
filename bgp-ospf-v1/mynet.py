#!/usr/bin/python

# bgp-ospf-v1.py

# Requires the bird routing daemon.
# Install with: 'sudo apt install bird'

# Initial code generated with Miniedit (~mininet/mininet/examples/miniexit.py)

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
import os

def myNetwork():
    os.system("rm -f /tmp/*.pid")

    net = Mininet(topo=None, build=False, ipBase='10.0.0.0/8')

    # Routers are Mininet hosts with IP forwarding enabled in the kernel
    info( '*** Add routers for AS65001\n')
    r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Two hosts
    info( '*** Add hosts for AS65001\n')
    h1 = net.addHost('h1', cls=Host, ip='192.168.1.1/24', defaultRoute='via 192.168.1.254')
    h2 = net.addHost('h2', cls=Host, ip='192.168.2.1/24', defaultRoute='via 192.168.2.254')
    h3 = net.addHost('h3', cls=Host, ip='192.168.3.1/24', defaultRoute='via 192.168.3.254')

    # Connect with links
    info( '*** Add links for AS65001\n')
    net.addLink(h1, r1) # eth0 eth0
    net.addLink(h2, r2) # eth0 eth0
    net.addLink(h3, r3) # eth0 eth0
    net.addLink(r1, r2) # eth1 eth1
    net.addLink(r1, r3) # eth2 eth1
    net.addLink(r2, r3) # eth2 eth2

    # Routers for AS65002
    info( '*** Add routers for AS65002\n')
    r4 = net.addHost('r4', cls=Node, ip='0.0.0.0')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r5 = net.addHost('r5', cls=Node, ip='0.0.0.0')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')
    r6 = net.addHost('r6', cls=Node, ip='0.0.0.0')
    r6.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Hosts
    info( '*** Add hosts for AS200\n')
    h4 = net.addHost('h4', cls=Host, ip='10.0.4.1/24', defaultRoute='via 10.0.4.254')
    h5 = net.addHost('h5', cls=Host, ip='10.0.5.1/24', defaultRoute='via 10.0.5.254')
    h6 = net.addHost('h6', cls=Host, ip='10.0.6.1/24', defaultRoute='via 10.0.6.254')

    # Connect with links
    info( '*** Add links for AS65002\n')
    net.addLink(h4, r4) # eth0 eth0
    net.addLink(h5, r5) # eth0 eth0
    net.addLink(h6, r6) # eth0 eth0
    net.addLink(r4, r5) # eth1 eth1
    net.addLink(r4, r6) # eth2 eth1
    net.addLink(r5, r6) # eth2 eth2

    # Link between AS65001 and 65002
    net.addLink(r3, r6) # eth3 eth3

    # Start the network
    info( '*** Starting network\n')
    net.build()

    # We need to manually set the IP addresses on the routers
    info( '*** Post configure switches and hosts\n')
    r1.cmd('ifconfig r1-eth0 inet 192.168.1.254 netmask 255.255.255.0')
    r1.cmd('ifconfig r1-eth1 inet 10.1.0.1 netmask 255.255.255.252')
    r1.cmd('ifconfig r1-eth2 inet 10.1.0.5 netmask 255.255.255.252')

    r2.cmd('ifconfig r2-eth0 inet 192.168.2.254 netmask 255.255.255.0')
    r2.cmd('ifconfig r2-eth1 inet 10.1.0.2 netmask 255.255.255.252')
    r2.cmd('ifconfig r2-eth2 inet 10.1.0.10 netmask 255.255.255.252')

    r3.cmd('ifconfig r3-eth0 inet 192.168.3.254 netmask 255.255.255.0')
    r3.cmd('ifconfig r3-eth1 inet 10.1.0.6 netmask 255.255.255.252')
    r3.cmd('ifconfig r3-eth2 inet 10.1.0.9 netmask 255.255.255.252')
    r3.cmd('ifconfig r3-eth3 inet 10.10.0.1 netmask 255.255.255.252')

    r4.cmd('ifconfig r4-eth0 inet 10.0.4.254 netmask 255.255.255.0')
    r4.cmd('ifconfig r4-eth1 inet 10.2.0.1 netmask 255.255.255.252')
    r4.cmd('ifconfig r4-eth2 inet 10.2.0.5 netmask 255.255.255.252')

    r5.cmd('ifconfig r5-eth0 inet 10.0.5.254 netmask 255.255.255.0')
    r5.cmd('ifconfig r5-eth1 inet 10.2.0.2 netmask 255.255.255.252')
    r5.cmd('ifconfig r5-eth2 inet 10.2.0.10 netmask 255.255.255.252')
    r5.cmd('ifconfig r5-eth3 inet 172.16.10.1 netmask 255.255.255.0')

    r6.cmd('ifconfig r6-eth0 inet 10.0.6.254 netmask 255.255.255.0')
    r6.cmd('ifconfig r6-eth1 inet 10.2.0.6 netmask 255.255.255.252')
    r6.cmd('ifconfig r6-eth2 inet 10.2.0.9 netmask 255.255.255.252')
    r6.cmd('ifconfig r6-eth3 inet 10.10.0.2 netmask 255.255.255.252')


    # Configure AS65001 routers
    info('*** Starting bird routing daemons\n')
    r1.cmd('bird -c bird-r1.conf -s /var/run/bird-r1.ctl')
    r2.cmd('bird -c bird-r2.conf -s /var/run/bird-r2.ctl')
    r3.cmd('bird -c bird-r3.conf -s /var/run/bird-r3.ctl')

    # Configure AS65002 routers
    r4.cmd('bird -c bird-r4.conf -s /var/run/bird-r4.ctl')
    r5.cmd('bird -c bird-r5.conf -s /var/run/bird-r5.ctl')
    r6.cmd('bird -c bird-r6.conf -s /var/run/bird-r6.ctl')

    # Start the CLI
    CLI(net)

    # We need to shut down bird cleanly before Mininet shutsdown.
    # If it fails, use 'sudo kill -9 <pid>' to kill left-over processes.
    info('*** Shutting down bird daemons\n')
    os.system("killall -9 bird")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
