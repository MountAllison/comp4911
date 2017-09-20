from socket import *

# TCP port we will listen for connections on
serverPort = 12000

# Create a listening socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the local IP address ('') and port number
serverSocket.bind(('', serverPort))

# Start listening on the socket
serverSocket.listen(1)

print 'The server is ready to receive'
while 1:
     # Accept a new connection. 
     # This creates a new socket that is 'connected' to the client
     connectionSocket, addr = serverSocket.accept()

     # Read data from client     
     sentence = connectionSocket.recv(1024)

     # Convert to uppercase and send back to client
     capitalizedSentence = sentence.upper()
     connectionSocket.send(capitalizedSentence)
 
     # Close socket
     connectionSocket.close()

