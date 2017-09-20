from socket import *

# Address (name) and port number of the process
# on the server we will send packets to
serverName = '10.0.0.2'
serverPort = 12000
server = (serverName, serverPort)

# Create a socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Get user input
message = raw_input('Input lowercase sentence:')

# Send message to server, read and display response
clientSocket.sendto(message, server)
response, serverAddress = clientSocket.recvfrom(2048)
print response

# Close the socket
clientSocket.close()
