#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "\nusage: $0 <router-name>\n"
    exit
fi

R=$1

echo "Starting zebra on ${R}"
/usr/lib/quagga/zebra -f zebra-${R}.conf -d \
  -i /tmp/zebra-${R}.pid -z /tmp/zserv-${R}.api
