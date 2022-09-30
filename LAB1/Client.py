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
    buff_cmd = cmd.split()
    if buff_cmd[0] not in commands:
        print("Command is not supported")
    elif buff_cmd[0] == commands[0]:
        if len(buff_cmd) < 3 or len(buff_cmd) > 3:
            print("Enter command according to the form: set <value> <value>")
        elif buff_cmd[1] < '0' or buff_cmd[1] > '100' or buff_cmd[2] < '0' or buff_cmd[2] > '100':
            print("Enter a value between 0 and 100")
        else:
            print(cmd)
    elif buff_cmd[0] == commands[1]:
        if len(buff_cmd) < 2 or len(buff_cmd) > 2:
            print("Enter command according to the form: setcanvas <value>")
        elif buff_cmd[1] < '0' or buff_cmd[1] > '100':
            print("Enter a value between 0 and 100")
        else:
            print(cmd)
    elif buff_cmd[0] == commands[2]:
        if len(buff_cmd) < 2 or len(buff_cmd) > 2:
            print("Enter command according to the form: setlight <value>")
        elif buff_cmd[1] < '0' or buff_cmd[1] > '100':
            print("Enter a value between 0 and 100")
        else:
            print(cmd)
    else:
        if len(buff_cmd) > 1:
            print("Enter command according to the form: get")
        else:
            print(cmd)

while True:
    cmd = input()
    cmd_handle(cmd)
    
