import socket
import threading
from time import sleep

HOST   = "127.0.0.1"
PORT = 55555
SERVER_ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSGAGE = "!DISCONNECT"

#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(SERVER_ADDR)

print(">>>>>Successful connection to the TCP_Server<<<<<")
print("List of supported commands")
print("set <value> <value> - Set shift canvan and light flow")
print("setcanvas <value> - Set shift canvas")
print("setlight <value> - Set light flow")
print("0 <= value <= 100")
print("get - Read the values of all parameters of the blind")
print("------------------------------------------------------\n")

commands = ("set", "setcanvas", "setlight", "get")

connected = True

def handle_send(client):
    global connected
    while True:
        cmd = input()

def cmd_handle(cmd):
    cmd = cmd.split()
    if cmd[0] not in commands:
        print("Command is not supported")
    

while True:
    cmd = input()
    cmd = cmd.split()
    print(len(cmd))
    
