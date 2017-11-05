import getpass
import sys
import telnetlib

host = 'localhost'
port = 2601
password = '123'

tn = telnetlib.Telnet(host, port)

if password:
    tn.read_until('Password: ')
    tn.write(password + '\n')

tn.write('show ip route\n')
tn.write('exit\n')

print tn.read_all()
