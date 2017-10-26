#!/usr/bin/python

# two-hosts.py

# Simple Mininet network with 1 router, 2 hosts
# h1 ---- r1 ---- h2

# Run with 'sudo python two-hosts.py'

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

###
### Setting addresses on Mininet hosts (which are used as routers here)
### can be tricky. The order that things are done matters. This example
### works because the first address for r1 is set when the host is
### created, and the second is set using addLink(). In particular, this
### is done *before* the network is started with net.build() in this case.
### You may have difficulty using this method for a more complex network.
###
### A technique that will always work is to set them using Linux commands
### (e.g. ifconfig) *after* the network has been started. This is what
### you saw in the in-class demonstratrion. To avoid having to do this
### manually every time the nework is started, you can use something like
### 'r1.cmd()' to run those commands after the network starts. Use the
### code in ospf-network.py as an example of how to do this.  Since you
### are not using a routing daemon (i.e. bird) to distribute routes,
### you will need to use the 'route' or 'ip' command to add static routes.
### Run 'man ip' and 'man route' for the manual pages.
###

def myNetwork():

    net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')

    # Routers are Mininet hosts with IP forwarding enabled in the kernel
    info( '*** Add switches\n')
    r1 = net.addHost('r1', cls=Node, ip='10.0.1.254/24')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Two hosts
    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.1/24', defaultRoute='via 10.0.1.254')
    h2 = net.addHost('h2', cls=Host, ip='10.0.2.1/24', defaultRoute='via 10.0.2.254')

    # Connect with links
    info( '*** Add links\n')
    net.addLink(h1, r1)
    net.addLink(r1, h2, params1={'ip': '10.0.2.254/24'})

    # Start the network
    info( '*** Starting network\n')
    net.build()

    info( '*** Post configure switches and hosts\n')
    ###
    ### Run Linux commands here to configure interfaces and static routes.
    ###

    # Run CLI and then shut down
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

