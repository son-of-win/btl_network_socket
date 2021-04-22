from socket import *
import base64

msg = "I love Computer Networks\r\n"
endmsg = ".\r\n"
cach = '-'*20
username =  "vuotnh.hrt@gmail.com"                 
password = "zovlyxhjlmahvesp" 
mailserver = ('mail.smtp2.go',2525) #Fill in start #Fill in end

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('smtp.gmail.com',587))

recv = clientSocket.recv(1024)
print("Message after connection request:" + recv.decode() + cach)
if recv[:3].decode() != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'helo huuvuot\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
print(recv1.decode() + cach)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# start tls
start_tls = 'starttls auth login\r\n'
clientSocket.send(start_tls.encode())
print(clientSocket.recv(1024).decode())

#login and authentication
auth_login = 'auth login\r\n'
clientSocket.send(auth_login.encode())
print(clientSocket.recv(1024).decode())
clientSocket.send(base64.b64encode(username.encode()) + b'\r\n')
print(clientSocket.recv(1024).decode())
clientSocket.send(base64.b64encode(password.encode()) + b'\r\n')
print(clientSocket.recv(1024).decode() + cach)
                                   
# Send MAIL FROM command and print server response.
mailFrom = "MAIL FROM:<vuotnh.hrt@gmail.com>\r\n"
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024)
print("After MAIL FROM command: "+recv2.decode() + cach)

# Send RCPT TO command and print server response.
rcptTo = "RCPT TO:<vuot2001.uet@gmail.com>\r\n"
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024)
print("After RCPT TO command: "+recv3.decode() + cach)


# Send DATA command and print server response.
data = "DATA\r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024)
print("After DATA command: "+recv4.decode() + cach)


# Send message data.
subject = "Subject: SMTP mail client testing \r\n" 
clientSocket.send(subject.encode())
message = input("Enter your message: \r\n")
clientSocket.send(message.encode() + b'\r\n')
clientSocket.send(endmsg.encode() + b'\r\n')
recv_msg = clientSocket.recv(1024)
print("Response after sending message body:"+recv_msg.decode() + cach)


# Send QUIT command and get server response.
clientSocket.send("QUIT\r\n".encode())
message=clientSocket.recv(1024)
print ('Mesage after quit:' + message.decode())
clientSocket.close()