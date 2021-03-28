import socket
host = '10.90.80.22'
port = 65432
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((host, port))
soc.listen()
conn, addr = soc.accept()
while conn:
    try:
        data = conn.recv(1024)
        print("Client" + ": "+ str(data,'utf-8'))
        message = input("you : ")
        conn.sendall(message.encode())

    finally:
        soc.close()