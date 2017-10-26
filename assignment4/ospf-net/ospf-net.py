#!/usr/bin/python

# ospf-net.py

# Mininet network with 2 hosts and 2 routers:
#  h1 ---- r1 ---- r2 ---- h2
#
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

#
# Generate dot code to draw the network with graphviz
#
# Copy the output and save in a file, e.g. mynet.dot
# Create a PNG file with: 'dot -Tpng -o mynet.png mynet.dot'
#
# If you have X forwarding (if 'xterm h1' etc. work, you do),
# you can view the image with 'xli mynet.png'
#
# Use 'apt install graphviz xli' to install Graphviz and xli
#
def make_dot(net):
    nodes = [x.name for x in net.hosts]
    links = [(x.intf1.name, x.intf2.name) for x in net.links]

    print 'digraph MyNet {'
    print '    rankdir="LR";'

    # Nodes
    for n in nodes:
        print '    ' + n + ' [labelfontsize=12];'

    # Links
    for l in links:
        node0, intf0 = l[0].split("-")
        node1, intf1 = l[1].split("-")
        print '    %s -> %s [dir=none, taillabel="%s", headlabel="%s", labelfontsize=8];' % (node0, node1, intf0, intf1)

    print '}'

#
# Build Mininet network with 2 hosts and 2 routers:
#   h1 ---- r1 ---- r2 ---- h2
#
def myNetwork():
    net = Mininet(topo=None, build=False, ipBase='10.0.0.0/8')

    # Routers are Mininet hosts with IP forwarding enabled in the kernel
    info( '*** Add routers\n')
    r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Two hosts
    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.1/24', defaultRoute='via 10.0.1.254')
    h2 = net.addHost('h2', cls=Host, ip='10.0.3.1/24', defaultRoute='via 10.0.3.254')

    # Connect with links
    info( '*** Add links\n')
    net.addLink(h1, r1)
    net.addLink(r1, r2)
    net.addLink(r2, h2)

    # Start the network
    info( '*** Starting network\n')
    net.build()
    info('*** Graphviz dotfile\n')
    make_dot(net)

    # We need to manually set the IP addresses on the routers
    info( '*** Post configure switches and hosts\n')
    r1.cmd('ifconfig r1-eth0 inet 10.0.1.254 netmask 255.255.255.0')
    r1.cmd('ifconfig r1-eth1 inet 10.0.2.254 netmask 255.255.255.0')
    r2.cmd('ifconfig r2-eth0 inet 10.0.2.253 netmask 255.255.255.0')
    r2.cmd('ifconfig r2-eth1 inet 10.0.3.254 netmask 255.255.255.0')

    # Run an instance of bird (configured to use OSPF) on each router.
    info('*** Starting bird routing daemons\n')
    r2.cmd('sleep 1')
    r1.cmd('bird -c bird-r1.conf -s /var/run/bird-r1.ctl')
    r2.cmd('bird -c bird-r2.conf -s /var/run/bird-r2.ctl')

    # Start the CLI
    CLI(net)

    # We need to shut down bird cleanly before Mininet shutsdown.
    # If it fails, use 'sudo kill -9 <pid>' to kill left-over processes.
    info('*** Shutting down bird daemons\n')
    r1.cmd('echo down | birdc -s /var/run/bird-r1.ctl')
    r2.cmd('echo down | birdc -s /var/run/bird-r2.ctl')
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
