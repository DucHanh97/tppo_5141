from concurrent.futures import thread
from email import message
import socket
import threading
from time import sleep

#client -> Server(listen) -> broadcast for all clients
#3: Receive: bytesAddressPair = UDPServerSocket.recvfrom(bufferSize) #Waiting here until receiving
#4: Send: UDPServerSocket.sendto(bytesToSend, addr)

clientlst   = []      #list client
ServerIP     = "127.0.0.1"
ServerPort   = 20001
bufferSize  = 1024
msgFromServer      = "Hello UDP Client"
bytesToSend        = str.encode(msgFromServer)

# Create a datagram socket (UDP)
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)      #1

#Bind to address and ip
UDPServerSocket.bind((ServerIP, ServerPort))                                          #2
print("UDP server up and listening")

def ReceiverThead():
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)         #Waiting here until receiving
        message = bytesAddressPair[0].decode('utf-8')
        address = bytesAddressPair[1]

        print(address)
        print(message)

        if address not in clientlst:
            clientlst.append(address)
        
        bytesToSend = str.encode(message)

        #Send to all clients (broadcast)
        for addr in clientlst:
            UDPServerSocket.sendto(bytesToSend, addr)


#Listen for incoming datagrams
thread = threading.Thread(target=ReceiverThead, args=())
thread.start()

while True:
    #do the main task here
    sleep(1)