# l2fw.py
# COMP 4911 - POX Firewall framework
# Based on code from Nick Feamster and Muhammad Shabaz

# Put this file, along with the firewall policy rule file in the directory
# /hone/mininet/pox/pox/comp4911

# Run it as follows:
#     Run mininet (specify that controller is remote), e.g.:
#         sudo mn --topo single,3 --mac --switch ovsk --controller remote
#
#     Run POX:
#         cd /home/mininet/pox
#         python pox.py forwarding.l2_learning comp4911.l2fw
#
# Add the --verbose switch to pox to print debug info

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import EventMixin, EventHalt
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
import os

# Set up logging, path to policy file
log = core.getLogger()
policyFile = "%s/pox/pox/comp4911/l2fw-policy.csv" % os.environ[ 'HOME' ]

# Simple firewall class for POX
class Firewall (EventMixin):

    # Example policy rules (instead use data read from policy file)
    # These rules will block traffic between 11:22:33:44:55:66 and aa:bb:cc:dd:ee:ff
    # Other traffic will be allowed (note: this is NOT how a real firewall should work!)
    # policy = [['11:22:33:44:55:66', 'aa:bb:cc:dd:ee:ff'],
    #           ['aa:bb:cc:dd:ee:ff', '11:22:33:44:55:66']]
    policy = []

    def __init__ (self):
        self.listenTo(core.openflow)
        log.info("Enabling Firewall Module")
        log.info("Loading rules from file: %s", policyFile)

        # Read rules from firewall policy file here and add them to
        # the policy list
        # << your code here >>

    #
    # These methods handle POX events.
    # See https://openflow.stanford.edu/display/ONL/POX+Wiki#POXWiki-HandlingEvents
    #

    # Handle the 'connection up' event when we first get a connection from a switch
    # Here we want to install rules in the to drop packets as specified in the
    # policy file
    def _handle_ConnectionUp (self, event):

        log.debug("ConnectionUp event")
        # Print out the datapath id of the switch we're getting a connection from.
        # Note that the ID of the first switch will be 00-00-00-00-00-01.
        # This is not a MAC address and should not be confused with the
        # MAC addresses of the hosts created by Mininet which will have a
        # MAC addressed of 00:00:00:00:00:01, 00:00:00:00:00:02, etc.,
        # Note: A 'datapath' is the same as a 'switch' (in OpenFlow)
        log.info("Installing rules on switch (datapath_id %s)", dpidToStr(event.dpid))

        # Iterate through the firewall rules and call installRule()
        # for each rule (pass event as the first argument)
        # << your code here >>


    # Install a flow rule on a switch to block packets from src -> dst
    def installRule(self, event, src, dst):
        # create a match object
        match = of.ofp_match()

        # What goes in the match object?
        # << your code here >>

        msg = of.ofp_flow_mod()                   # create a flowmod message
        msg.match = match                         # specify the match object
        msg.priority = 0xFFFF                     # highest priority
        msg.idle_timeout = of.OFP_FLOW_PERMANENT  # Keep these flow rules forever
        msg.hard_timeout = of.OFP_FLOW_PERMANENT
        event.connection.send(msg)                # send flowmod msg to switch
        log.info("Installing firewall rule for src=%s, dst=%s" % (src, dst))
        log.debug(msg)


    # This handler is not required to implement the firewall, but is useful to see 
    # packets that arrive at the controller
    # Handle a 'packet in' event for a *new* flow (i.e. the first time we see a packet 
    # that doesn't match an existing flow)
    # See https://openflow.stanford.edu/display/ONL/POX+Wiki#POXWiki-Workingwithpackets%3Apox.lib.packet
    # for more on working with packets in POX
    # Run POX in verbose mode (--verbose) to see debug output
    def _handle_PacketIn(self, event):

        # 'packet' is an Ethernet frame. Fields are: dst, src, type, effective_type
        packet = event.parsed
        #log.debug("PacketIn: dst=%s, src=%s, type=%s" % (packet.dst, packet.src, packet.type))
        log.debug("PacketIn event: %s" % packet)


def launch ():
    # Starting the Firewall module
    core.registerNew(Firewall)
