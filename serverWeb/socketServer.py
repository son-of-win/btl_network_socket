from socket import *
import sys

hostname = "192.168.1.104"
port = 1310
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((hostname, port))
serverSocket.listen(1)
while True:
    print('ready to server.....')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)
        print(message)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        connectionSocket.send(b'HTTP/1.0 200 OK\r\n\r\r\n')
        for i in range(0, len(outputdata)):
            print(outputdata[i])
            connectionSocket.send(bytes(outputdata[i],'utf-8'))
        connectionSocket.close()

    except IOError:
        connectionSocket.send(b'404 Not Found')
        connectionSocket.close()

serverSocket.close()