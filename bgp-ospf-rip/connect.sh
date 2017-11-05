#!/bin/sh

# Connect to the zebra vty on a router.
# vtysh does not work with multiple instances of Quagga daemons.

if [ "$#" -ne 1 ]; then
    echo "\nusage: $0 <router-name>\n"
    exit
fi

~/mininet/util/m $1 "telnet localhost 2601"
