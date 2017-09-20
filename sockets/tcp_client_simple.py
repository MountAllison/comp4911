from socket import *

# Address (name) and port of the server process
# we will connect to
serverName = '10.0.0.2'
serverPort = 12000
server = (serverName, serverPort)

# Create socket and connect to server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(server)

# Get user input
message = raw_input('Input lowercase sentence:')

# Send message, read response
clientSocket.send(message)
response = clientSocket.recv(1024)

# Print response from server
print 'From Server:', response

# Close socket
clientSocket.close()

