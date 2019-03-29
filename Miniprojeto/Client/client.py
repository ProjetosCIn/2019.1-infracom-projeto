# Author: Thiago Augusto - tasm2
# IF678 - Infraestrutura de Comunicação 2019.1 
# Miniprojeto Sockets

import sys
import socket
import traceback
import os

serverName = "localhost"
serverPort = 2080

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    try:
        clientSocket.connect((serverName,serverPort))
        getClientData()
    except Exception:
        print("I could not connect to the server, this is the problem:")
        print(Exception)

def getClientData():
    try:
        print("Hello, welcome to DOWNLOAD-UPLOAD\n")
        while 1:
            print("\nWhat do you want to do?\
                            \n\t1-Download\n\t2-Upload\n\t3-GETPROG(Download and Execute)")
            print("Type anything else to get out of the program\n")
            choice = input(":")

            if(choice == "1" or choice == "3"):
                print("\nWhat is the file you want to Download?\n")
                fileName = input(":")
                
                print("\nWhat is the name you want to save it?\n")
                outputName = input(":")
                
                header = "GET /"+ fileName +" HTTP/1.1\n"
                contentLength = "Content-Length: 0\n"
                header = header + contentLength
                clientSocket.sendall(header.encode()) 
                
                #Only to send back the response from getting header
                responseHeader = clientSocket.recv(1024).decode()
                
                clientSocket.sendall(header.encode())
                responseHeader = responseHeader.split('\n')
                responseStatus = responseHeader[0].split(' ')[1]
                contentLength = int(responseHeader[1].split(' ')[1])

                if(responseStatus == "200"):   
                    # The data are arriving in chuncks of bytes, in bits encoded
                    response = b''
                    while True:
                        data = clientSocket.recv(1024)
                        if not data: break
                        response += data
                        if(len(response) >= contentLength): break
                    with open(outputName, 'wb') as f:
                        f.write(response)
                    print("\n"+ outputName + " file created!")
                elif(responseStatus == "404"):
                    print("\nError 404\nTry again!\n")
                
                if(choice == "3"):
                    os.system('chmod +x ' + outputName)
                    os.system('./' + outputName)
                
            elif(choice == "2"):
                print("\nWhat is the file you want to Upload?\n")
                fileName = input(":")

                header = "SEND /"+ fileName +" HTTP/1.1\n"
                contentLength = "Content-Length: "+ str(fileSize(fileName)) + "\n"
                header = header + contentLength
                clientSocket.sendall(header.encode()) 
                clientSocket.recv(1024)
                
                sendFile(fileName, clientSocket)
                print("\nYour file ", fileName, " was uploaded!")
            
            else:
                print("See ya!")
                break

        clientSocket.close()

    except KeyboardInterrupt:
        escape = True
    except Exception as e:
        print(traceback.print_tb(e.__traceback__))
        print ("Unexpected error:", sys.exc_info()[0])
        clientSocket.close()


    clientSocket.close()
    print("\nBye bye :)")

def sendFile(fileName, socket):

    with open(fileName, 'rb+') as f:
        data = f.read()
        socket.sendall(data)

def fileSize(fname):
    return os.stat(fname).st_size

main()
