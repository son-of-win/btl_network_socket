from threading import Thread

class ClientThread(Thread):
    def __init__(self, ip, port,conn):
        super().__init__()
        self.ip = ip
        self.port = port
        self.conn = conn
        self.name = ""
        print("New server connect: ", ip, port)
        conn.send(bytes('Connect successfully','utf-8'))
    def run(self):
        name = self.conn.recv(1024).decode()
        self.name = name
        while True:
            data = self.conn.recv(2048).decode()
            if(data == 'exit'):
                self.conn.close()
                break
            print(name + ":", data)
            inputUser = input("> ")
            if(inputUser == 'exit'):
                break
            self.conn.send(bytes(inputUser,'utf-8'))
        self.conn.close()
   