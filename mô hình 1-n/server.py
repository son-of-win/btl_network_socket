import socket
import threading
from clientThread import ClientThread
host = '192.168.1.108'
port = 65432
clients = []
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
soc.bind((host, port))

print("Server is listening......")
while True:
    soc.listen()
    (conn, (ipaddr, port)) = soc.accept()
    print('New user: ',ipaddr)
    newClient = ClientThread(ipaddr, port,conn)
    newClient.start()
    clients.append(newClient)

for client in clients:
    client.join()    