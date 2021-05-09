from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) *2
    count = 0

    while count < countTo:
        # thisVal = ord(string[count + 1]*256) + ord(string[count])
        thisVal = string[count + 1]*256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum # answer = -answer - 1
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        startedSelect = time.time() # thời điểm bắt đầu nhận
        whatReady = select.select([mySocket],[],[],timeLeft)  # chờ đến khi mySocket được thiết lập, ko quá thời gian timeLeft
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        icmpHeader = recPacket[20:28]
        icmpType, code, mychecksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
        
        # option 2
        if icmpType == 3:    # type on response : destination unreachable
            if code == 0:   
                return "Destination network unreachable."
            elif code == 1:
                return "Destination host unreachable."


        print("-"*20)
        print('Respone ICMP packet')
        print('icmpType: ',icmpType)
        print('code: ',code)
        print('checksum: ', mychecksum)  # khi capture gói tin bằng wireshark, checksum = 0xdabc => mychecksum = 0xbcda do dòng 79
        print('packetID: ', packetID)
        print(" ")

        if type != 8 and packetID == ID:
            bytesInDouble = struct.calcsize('d') # caculate size for double var (8 byte)
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent

        timeLeft = timeLeft - howLongInSelect

        if timeLeft <= 0:
            return "Request timed out."

    
def sendOnePing(mySocket, destAddr, ID):
    # header is type (8), code(8), checksum(16),id(16), sequence(16)
    myChecksum = 0
    #Make a dummy header with a 0 checksum
    #struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST,0,myChecksum,ID,1) # convert param to byte
    data = struct.pack("d",time.time())
    #Caculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    #get the right checksum, and put in the header
    if sys.platform == "darwin" :
        myChecksum = htons(myChecksum) & 0xffff
    # Convert 16-bit integers from host to network byte order
    else:
        myChecksum = htons(myChecksum)  # reverse the string in bytes

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST,0,myChecksum,ID,1)
    packet = header + data
    mySocket.sendto(packet, (destAddr,1)) # AF_INET address must be tuple , not str
    #Both LISTS and TUPLES consist of a number of objects
    #which can be referenced by their position number within the object

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    #create socket here
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF #Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay


def ping(host, timeout = 1):
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    #send ping request to a server separated by approximately one second
    while 1:
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1) # one second
    return delay

ping("169.254.157.237")