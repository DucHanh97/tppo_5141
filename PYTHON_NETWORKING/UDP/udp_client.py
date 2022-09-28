from email import message
import socket
import threading

#Client -> Server(listen) -> Send back to client
#UDP server and client: use the same functions

serverAddressPort       = ("127.0.0.1", 20001)
buffSize                = 1024

#C1
#ClientIP                = "127.0.0.1"
#ClientPort              = 20015

#C2:
msgFromClient           = "Hello Server"
bytesToSend             = str.encode(msgFromClient)

#Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)      #1

#Bind to address and ip
#C1:
#UDPClientSocket.bind((ClientIP, ClientPort))                                        #2

#C2:
UDPClientSocket.sendto(bytesToSend, serverAddressPort)            #Create Random Port Number and Get Current System IP

print("UDP CLIENT up and listening")

def ReceiveThread():
    while True:
        bytesAddressPair = UDPClientSocket.recvfrom(buffSize)          #Waiting here until receiving
        message = bytesAddressPair[0].decode('utf-8')
        address = bytesAddressPair[1]

        print(address)
        print(message)

#Listen for incoming datagrams
thread = threading.Thread(target=ReceiveThread, args=())
thread.start()

while True:
    msg = input()
    bytesToSend = str.encode(msg)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
