import socket

import argparse

serverName = "localhost"
serverPort = 2080

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

parser = argparse.ArgumentParser()
parser.add_argument('--message', '-d', type=str,
                    help='file.txt')
args = parser.parse_args()

print (args.message)

try:
    clientSocket.connect((serverName,serverPort))
except Exception:
    print(Exception)

try:
    sentence = input("Input lowercase sentence: ")
    #sentence = args.message
    clientSocket.send(sentence.encode())

    modifiedSentence = clientSocket.recv(1024)

    print("From Server: ", modifiedSentence.decode())

    clientSocket.close()

except KeyboardInterrupt:
    escape = True
except Exception:
    clientSocket.close()


clientSocket.close()
print("\nBye bye :)")
