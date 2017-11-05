#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "\nusage: $0 <router-name>\n"
    exit
fi

R=$1

echo "Starting bgpd on ${R}"
/usr/lib/quagga/bgpd -f bgpd-${R}.conf -d \
   -i /tmp/bgpd-${R}.pid -z /tmp/zserv-${R}.api
