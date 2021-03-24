import socket
host = '192.168.1.104'
port = 65432
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((host, port))
while True:
    message = input("Nhap:")
    soc.sendall(message.encode())
    data = soc.recv(1024)
    print("Server: " + str(data,'utf-8'))
