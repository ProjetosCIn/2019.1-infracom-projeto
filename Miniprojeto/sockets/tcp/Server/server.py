import sys
import itertools
import socket
from socket import socket as Socket
import os

def main():

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to address
        # (arg1, arg2) HOST, PORT
        server_socket.bind(('', 2080))

        # Enable a server to accept connections
        # (arg) number of unaccepted connections
        server_socket.listen(1)

        print("server ready")


        (clientSocket, address) = server_socket.accept()
        while True:
            
            print("rodandoo")
            print("Client:", clientSocket)
            print("Address:", address)

            request = clientSocket.recv(1024)
            print(request)
            request = request.decode()
            if len(request) > 0:
                (method, fileName, content) = http_handle(request)
                print(method, fileName)

                # Check if file exists
                exists = os.path.isfile(fileName)
                if not exists:
                    method = "404"
                print(method)

                if(method == 'GET'):
                    responseHeader = \
                    "HTTP/1.1 200 OK\n"+\
                    "Content-Length: " + str(fileSize(fileName)) +'\n'                 
                    print(fileSize(fileName))
                    sendHeader(responseHeader, clientSocket)
                    clientSocket.recv(1024)
                    sendFile(fileName, clientSocket)
                elif(method == 'SEND'):
                    responseHeader = "HTTP/1.1 200 OK\n"
                    clientSocket.send(responseHeader.encode('utf8'))
                    saveFile(fileName, content)
                else:
                    responseHeader = "HTTP/1.1 404 Not Found\n"
                    contentLength = "Content-Length: 0\n"
                    print("Here")
                    clientSocket.sendall(responseHeader.encode())
                    clientSocket.sendall(contentLength.encode())

                print("\n\nReceived request")
                print("======================")
                print(request.rstrip())
                print("======================")


                # print("\n\nReplied with")
                # print("======================")
                # #print(reply.rstrip())
                # print("======================")

            #clientSocket.close()
            print("DOEN")

    return 0

def sendHeader(header, socket):
    socket.sendall(header.encode())

def fileSize(fname):
    return os.stat(fname).st_size

def sendFile(fileName, socket):
    

    with open(fileName, 'rb+') as f:
        
        data = f.read()
        socket.sendall(data)
        print("Sending...\n")
        print(len(data), " bytes")
        
    return True

def saveFile(fileName, content):
    with open(fileName, 'wb') as f:
        f.write(content)

def http_handle(request_string):
    """Given a http request return its arguments
    method, fileName and content
    Only send content if it is upload
    Both request and response are unicode strings with platform standard
    line endings.
    """
    header = request_string.split(' ')
    print(header)
    return (header[0], header[1][1:], header[2])

    contents = ''
    with open(request_string, 'r') as file:
        contents = file.read()

    print('contents: ' + contents)


    return contents

if __name__ == "__main__":
    sys.exit(main())
