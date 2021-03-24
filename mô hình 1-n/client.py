import socket
import sys 
import select
host = '192.168.1.108'
port = 65432
name = input("Enter your name: ")
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((host, port))
soc.send(bytes(name, 'utf-8'))
while True:
    data = soc.recv(1024).decode()
    print("Server: ", data)
    message = input('> ')
    if message == 'exit':
        break
    soc.send(bytes(message,'utf-8'))
soc.close()