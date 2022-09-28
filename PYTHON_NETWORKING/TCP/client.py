import socket
import threading
from time import sleep

PORT = 55555
SERVER = "192.168.194.117"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSGAGE ="!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

connected = True

def handle_rev(client):
    global connected
    while connected:
        msg = client.recv(30).decode(FORMAT)
        print(msg)
        #print(len(msg))
    client.close()
    
def handle_send(client):
    global connected
    while True:
        msg = input()
        send("[Client 01] " + msg)      #[Client 01] !DISCONNECT
        if msg == DISCONNECT_MESSGAGE:
            connected = False
            break

def send(msg):
    message = msg.encode(FORMAT)
    message += b' ' * (30 - len(message))
    client.send(message)

thread1 = threading.Thread(target=handle_rev, args=(client, ))
thread1.start()

thread2 = threading.Thread(target=handle_send, args=(client, ))
thread2.start()

while connected:
    #Do main ttask
    sleep(2)
