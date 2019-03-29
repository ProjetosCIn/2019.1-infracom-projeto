# Author: Thiago Augusto - tasm2
# IF678 - Infraestrutura de Comunicação 2019.1 
# Miniprojeto Sockets

import sys
import itertools
import socket
from socket import socket as Socket
import os

def main():

    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to address
        # (arg1, arg2) HOST, PORT
        server_socket.bind(('', 2080))

        # Enable a server to accept connections
        # (arg) number of unaccepted connections
        server_socket.listen(1)
        print("Server On")
        while True:            
            # Get the clientSocket and end it when it is done
            with server_socket.accept()[0] as clientSocket:
                # Keeps the connection awake while the client is on
                print("\nNew Client")
                while True:
                    # HTTP requests
                    request = clientSocket.recv(1024)
                    request = request.decode()
                    if not request: break
                    
                    print("\nRequest", request)
                    
                    (method, fileName, contentSize) = httpHandle(request)
                    
                    if(method == "GET"):
                        # Check if file exists
                        exists = os.path.isfile(fileName)
                        if not exists:
                            method = "404"

                    if(method == 'GET'):
                        responseHeader = \
                        "HTTP/1.1 200 OK\n"+\
                        "Content-Length: " + str(fileSize(fileName)) +'\n'                 
                        sendHeader(responseHeader, clientSocket)
                        clientSocket.recv(1024)
                        sendFile(fileName, clientSocket)
                        print("File ", fileName, " sent to client!")
                    elif(method == 'SEND'):
                        responseHeader = "HTTP/1.1 200 OK\n"
                        clientSocket.send(responseHeader.encode())
                        receiveFile(fileName, int(contentSize), clientSocket)
                        print("File ", fileName, " saved in folder files!")
                    else:
                        responseHeader = "HTTP/1.1 404 Not Found\n"
                        contentLength = "Content-Length: 0\n"
                        clientSocket.sendall(responseHeader.encode())
                        clientSocket.sendall(contentLength.encode())
                clientSocket.close()
            print("Client has left")

    return 0

def sendHeader(header, socket):
    socket.sendall(header.encode())

def fileSize(fname):
    return os.stat(fname).st_size

def sendFile(fileName, socket):
    with open(fileName, 'rb+') as f:
        data = f.read()
        socket.sendall(data)

def receiveFile(fileName, fileSize, socket):
    response = b''
    while True:
        data = socket.recv(1024)
        if not data: break
        response += data
        if(len(response) >= fileSize): break
    with open('files/' + fileName, 'wb') as f:
        f.write(response)

def httpHandle(requestString):
    """Given a http request return its arguments
    method, fileName and content"""
    header = requestString.split('\n')
    header = [n.split(' ') for n in header]
    return (header[0][0], header[0][1][1:], header[1][1])

if __name__ == "__main__":
    sys.exit(main())
