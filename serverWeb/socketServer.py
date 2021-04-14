from socket import *
import sys

hostname = "10.90.80.22"
port = 1310
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((hostname, 1310))
serverSocket.listen(1)
while True:
    print('ready to server.....')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(4096)
        print(message)
        filename = message.split()[1]
        if not filename:
            f = open("C:\\Users\\Admin\\Documents\\network\\btl_network_socket\\serverWeb\\index.html","rb")
        else:
            f = open(filename[1:].decode('utf-8'),'rb')
        # 
        outputdata = f.read()
        f.close()
        header = "'HTTP/1.1 404 OK\r\n\r\r\n"
        content = "Context-Type: text/html \n\n"
        data = header.encode('utf-8')
        data += content.encode("utf-8")
        data = data + outputdata
        connectionSocket.send(data)
        connectionSocket.close()

    except IOError:
        connectionSocket.send(b'404 Not Found')
        connectionSocket.close()

serverSocket.close()