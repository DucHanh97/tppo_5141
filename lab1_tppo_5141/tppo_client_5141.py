import socket
import threading
from time import sleep

HOST   = input("Enter server IP-Address: ")
PORT = int(input("Enter server PORT: "))
SERVER_ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSGAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SERVER_ADDR)

print(">>>>>Successful connection to the TCP_Server<<<<<")
print("**[List of supported commands]**")
print("> set <value> <value> - Set shift canvan and light flow")
print("> setcanvas <value> - Set shift canvas")
print("> setlight <value> - Set light flow")
print("> 0 <= value <= 100")
print("> get - Read the values of all parameters of the blind")
print("> ", DISCONNECT_MESSGAGE, " - disconnect to the TCP_Server")
print("------------------------------------------------------\n")
print("Enter a command\n")
commands = ("set", "setcanvas", "setlight", "get", DISCONNECT_MESSGAGE)

connected = True

def handle_recv(client):
    global connected
    while connected:
        rx_data = client.recv(50).decode(FORMAT)
        print(rx_data)
    client.close()

def handle_send(client):
    global connected
    while True:
        cmd = input()
        if cmd == DISCONNECT_MESSGAGE:
            send(DISCONNECT_MESSGAGE)
            connected = False
            break
        else:
            cmd_handle(cmd)

def send(cmd):
    command = cmd.encode(FORMAT)
    client.send(command)

def strtoint(str):
    try:
        return(int(str))    
    except:
        return -1

def xml_cmd_toSend(cmd,arg1, arg2):
    xml_data = f"<command><cmd>{cmd}</cmd><arg1>{arg1}</arg1><arg2>{arg2}</arg2></command>"
    return xml_data

def cmd_handle(cmd):
    xml_data = ""
    buff_cmd = cmd.split()
    if buff_cmd[0] not in commands:
        print("Command is not supported")
    elif buff_cmd[0] == commands[0]:
        if len(buff_cmd) < 3 or len(buff_cmd) > 3:
            print("Enter command according to the form: set <value> <value>")
        elif strtoint(buff_cmd[1]) < 0 or strtoint(buff_cmd[1]) > 100 or strtoint(buff_cmd[2]) < 0 or strtoint(buff_cmd[2]) > 100:
            print("Enter values between 0 and 100")
        else:
            xml_data = xml_cmd_toSend(buff_cmd[0], buff_cmd[1], buff_cmd[2])
    elif buff_cmd[0] == commands[1]:
        if len(buff_cmd) < 2 or len(buff_cmd) > 2:
            print("Enter command according to the form: setcanvas <value>")
        elif strtoint(buff_cmd[1]) < 0 or strtoint(buff_cmd[1]) > 100:
            print("Enter a value between 0 and 100")
        else:
            xml_data = xml_cmd_toSend(buff_cmd[0], buff_cmd[1], "NULL")
    elif buff_cmd[0] == commands[2]:
        if len(buff_cmd) < 2 or len(buff_cmd) > 2:
            print("Enter command according to the form: setlight <value>")
        elif strtoint(buff_cmd[1]) < 0 or strtoint(buff_cmd[1]) > 100:
            print("Enter a value between 0 and 100")
        else:
            xml_data = xml_cmd_toSend(buff_cmd[0], "NULL", buff_cmd[1])
    else:
        xml_data = xml_cmd_toSend(buff_cmd[0], "NULL", "NULL")
    send(xml_data)


thread1 = threading.Thread(target=handle_recv, args=(client, ))
thread1.start()

thread2 = threading.Thread(target=handle_send, args=(client, ))
thread2.start()

while connected:
    sleep(2)
