from socket import *
from string import ascii_lowercase

# We need the address (name) and port number of the
# server process we will send data to
serverName = '10.0.0.2'
serverPort = 12000
server = (serverName, serverPort)

# Loop through the ASCII letters and send each to the server
# to be converted to uppercase
for c in ascii_lowercase:
    # Create a TCP socket and connect to the server
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(server)

    # Send a character, read response, print it
    clientSocket.send(c)
    response = clientSocket.recv(2048)
    print response

    # Close the socket
    clientSocket.close()
