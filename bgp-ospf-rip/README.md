# OSPF and BGP example with Mininet

Mininet example using BGP to route between two OSPF networks,
using the Quagga routing suite (http://www.nongnu.org/quagga/).

To ensure that the zebra ospfd and bgpd instances run properly
in their Mininet virtual hosts (routers), the configuration file,
pid file, and zebra socket must be unique for each instance.
See the start-zebra.shm start-ospfd.sh, and start-bgpd.sh scripts.
