# Author: Thiago Augusto - tasm2
# IF678 - Infraestrutura de Comunicação 2019.1 

import sys
import socket
import traceback

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
        while 1:
            print("Hello, welcome to DOWNLOAD-UPLOAD\n")
            print("What do you want to do?\
                            \n\t1-Download\n\t2-Upload")
            print("Type anything else to get out of the program\n")
            choice = int(input(":"))
            
            if(choice == 1):
                print("\nWhat is the file you want to Download?\n")
                fileName = input(":")
                
                print("\nWhat is the name you want to save it?\n")
                outputName = input(":")
                
                print("GO TO CONNET")
                #sentence = args.message
                #clientSocket.sendall("GET / HTTP/1.1\r\n\r\n")
                print("B TO SEND")
                header = "GET /"+ fileName +" HTTP/1.1"
                print("GOIN TO SEND")
                print(header)
                clientSocket.sendall(header.encode()) #utf8
                #clientSocket.send(fileName.encode())
                print("OI")
                responseHeader = clientSocket.recv(1024).decode()
                print("Response", responseHeader)
                clientSocket.sendall(header.encode())
                responseHeader = responseHeader.split('\n')
                responseStatus = responseHeader[0].split(' ')[1]
                contentLength = int(responseHeader[1].split(' ')[1])

                print("Status", responseStatus,"Length", contentLength)
                # It recieve a ok data load
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
                    print(outputName + " file created!")
                elif(responseStatus == "404"):
                    print("Error 404\nTry again!\n")

                
            elif(choice == 2):
                pass
            else:
                print("See ya!")


        clientSocket.close()

    except KeyboardInterrupt:
        escape = True
    except Exception as e:
        print(traceback.print_tb(e.__traceback__))
        print ("Unexpected error:", sys.exc_info()[0])
        clientSocket.close()


    clientSocket.close()
    print("\nBye bye :)")

main()
