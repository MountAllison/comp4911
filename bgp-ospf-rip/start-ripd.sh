#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "\nusage: $0 <router-name>\n"
    exit
fi

R=$1

echo "Starting ripd on ${R}"
/usr/lib/quagga/ripd -f ripd-${R}.conf -d \
  -i /tmp/ripd-${R}.pid -z /tmp/zserv-${R}.api
