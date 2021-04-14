import socket
import os
host = '10.90.80.22'
port = 1310
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((host, port))
request = "GET /index.html HTTP/1.1\r\nHost: " +host + ":" + str(port) + "\r\n\r\n"
soc.send(request.encode())
dataRecv = ""
while True:
    data = soc.recv(1024)
    if not data:
        break
    dataRecv += str(data,'utf-8')
    print("Server: " + str(data,'utf-8'))

