from socket import *
from string import ascii_lowercase

# Address (name) and port number of the
# server process we will send packets to
serverName = '10.0.0.2'
serverPort = 12000
server = (serverName, serverPort)

# Create a socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Loop through the ASCII letters and send each to the server
# to be converted to uppercase
for c in ascii_lowercase:
    # Send packet, read respose, print it
    clientSocket.sendto(c, server)
    response, serverAddress = clientSocket.recvfrom(2048)
    print response

# Close the socket
clientSocket.close()

