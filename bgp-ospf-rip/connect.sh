#!/bin/sh
if [ "$#" -ne 1 ]; then
    echo "\nusage: $0 <router-name>\n"
    exit
fi

~/mininet/util/m $1 "telnet localhost 2601"
