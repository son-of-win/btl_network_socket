from socket import *

msg = "\r\n My email's content! "
endmsg = "\r\n.\r\n"

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('smtp.gmail.com',587))

recv = clientSocket.recv(1024)
recv = recv.decode()
print("Message after connection request: " + recv)
if recv[:3] != '220':
    print('220 reply not received from server')

helloCommand = 'HELO huuvuot\r\n'
clientSocket.send(helloCommand.encode())
recv1 = clientSocket.recv(1024)
recv1 = recv1.decode()
print("Message after Hello command: " + recv1)
if recv1[:3] != '250':
    print('250 reply not received from server')

# TLS
clientSocket.send(('starttls\r\n').encode())
recv_tls = clientSocket.recv(1024)
print(recv_tls.decode())

# send mail from command and print server response
mailFrom = "MAIL FROM: <huuvuot2001@gmail.com>\r\n"
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024)
recv2 = recv2.decode()
print("AFTER mail from command:" + recv2)

#send RCPT to command and print server response
rcptTo = " RCPT TO: <vuot2001.uet@gmail.com>\r\n"
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv()
recv3 = recv3.decode()
print("After RCPT to command: " + recv3)

# send data command and print server response
data = "DATA \r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024)
recv4 = recv4.decode()
print("After DATA command: "+ recv4)

# send message data
clientSocket.send(msg.encode())

#send message end with a single period
clientSocket.send(endmsg.encode())
recv_msg = clientSocket.recv(1024)
print("Response after sending message body: " + recv_msg.decode())

#send QUIT command and get response from server
quit = 'QUIT\r\n'
clientSocket.send(quit.encode())
recv5 = clientSocket.recv(1024)
print(recv5.decode())
clientSocket.close()
