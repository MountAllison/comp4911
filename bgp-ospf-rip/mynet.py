#!/usr/bin/python

# as.py

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
import time

def myNetwork():
    # Clean up any old log and pid files
    os.system("rm -f /tmp/zebra-r*.log /tmp/ospfd-r*.log /tmp/bgpd-r*.log")
    os.system("rm -f /tmp/zebra-r*.pid /tmp/ospfd-r*.pid /tmp/bgpd-r*.pid")

    net = Mininet(topo=None, build=False, ipBase='10.0.0.0/8')

    # Routers are Mininet hosts with IP forwarding enabled in the kernel
    info( '*** Add routers for AS65001\n')
    r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    # A host attached to each router
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
    info( '*** Add hosts for AS65002\n')
    h4 = net.addHost('h4', cls=Host, ip='176.16.4.1/24', defaultRoute='via 176.16.4.254')
    h5 = net.addHost('h5', cls=Host, ip='176.16.5.1/24', defaultRoute='via 176.16.5.254')
    h6 = net.addHost('h6', cls=Host, ip='176.16.6.1/24', defaultRoute='via 176.16.6.254')

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

    # Configure AS65001 routers
    # Run an instance of bird (configured to use OSPF) on each router.
    info('*** Starting zebra routing daemons\n')
    time.sleep(1)

    r1.cmd('./start-zebra.sh r1')
    r1.cmd('./start-ospfd.sh r1')
    r2.cmd('./start-zebra.sh r2')
    r2.cmd('./start-ospfd.sh r2')
    r3.cmd('./start-zebra.sh r3')
    r3.cmd('./start-ospfd.sh r3')

    r4.cmd('./start-zebra.sh r4')
    r4.cmd('./start-ripd.sh r4')
    r5.cmd('./start-zebra.sh r5')
    r5.cmd('./start-ripd.sh r5')
    r6.cmd('./start-zebra.sh r6')
    r6.cmd('./start-ripd.sh r6')

    r3.cmd('./start-bgpd.sh r3')
    r6.cmd('./start-bgpd.sh r6')

    # Start the CLI
    CLI(net)

    # We need to shut down bird cleanly before Mininet shutsdown.
    # If it fails, use 'sudo kill -9 <pid>' to kill left-over processes.
    info('*** Shutting down quagga daemons\n')
    os.system("killall -9 ospfd ripd bgpd zebra")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
