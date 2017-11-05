#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "\nusage: $0 <router-name>\n"
    exit
fi

R=$1

echo "Starting ospfd on ${R}"
/usr/local/sbin/ospfd -f ospfd-${R}.conf -d \
  -i /tmp/ospfd-${R}.pid -z /tmp/zserv-${R}.api
