import socketio
import requests

commands = ("set", "setcanvas", "setlight", "get")

client_io = socketio.Client()

def get_parameter():
    global host
    global port
    api_url = f"http://{host}:{port}/blinds/infor"
    return requests.get(api_url)

def set_parameter(parameter, value):
    global host
    global port
    api_url = f"http://{host}:{port}/blinds?{parameter}={value}"
    return requests.get(api_url)

def set_both_parameters(param_1, value_1, param_2, value_2):
    global host
    global port
    api_url = f"http://{host}:{port}/blinds?{param_1}={value_1}&{param_2}={value_2}"
    return requests.get(api_url)

def strtoint(str):
    try:
        return(int(str))
    except:
        return -1

@client_io.event
def connect():
    global host
    global port
    print(">>>>>Successful connection to the TCP_Server<<<<<")
    print("**[List of supported commands]**")
    print("> set <value> <value> - Set shift canvan and light flow")
    print("> setcanvas <value> - Set shift canvas")
    print("> setlight <value> - Set light flow")
    print("> 0 <= value <= 100")
    print("> get - Read the values of all parameters of the blind")
    print("------------------------------------------------------\n")
    print("Enter a command\n")
    while True:
        cmd = input()
        buff_cmd = cmd.split()
        if buff_cmd[0] not in commands:
            print("Command is not supported")
        elif buff_cmd[0] == commands[0]:
            if len(buff_cmd) < 3 or len(buff_cmd) > 3:
                print("Enter command according to the form: set <value> <value>")
            elif strtoint(buff_cmd[1]) < 0 or strtoint(buff_cmd[1]) > 100 or strtoint(buff_cmd[2]) < 0 or strtoint(buff_cmd[2]) > 100:
                print("Enter values between 0 and 100")
            else:
                response = set_both_parameters("canvas",buff_cmd[1],"light", buff_cmd[2])
                print(f"[Parameters have set]: ", response.json()[0], response.json()[1])
        elif buff_cmd[0] == commands[1]:
            if len(buff_cmd) < 2 or len(buff_cmd) > 2:
                print("Enter command according to the form: setcanvas <value>")
            elif strtoint(buff_cmd[1]) < 0 or strtoint(buff_cmd[1]) > 100:
                print("Enter a value between 0 and 100")
            else:
                response = set_parameter("canvas", buff_cmd[1])
                print(f"[Parameter has set]: ", response.json()[0])
        elif buff_cmd[0] == commands[2]:
            if len(buff_cmd) < 2 or len(buff_cmd) > 2:
                print("Enter command according to the form: setlight <value>")
            elif strtoint(buff_cmd[1]) < 0 or strtoint(buff_cmd[1]) > 100:
                print("Enter a value between 0 and 100")
            else:
                response = set_parameter("light", buff_cmd[1])
                print(f"[Parameter has set]: ", response.json()[1])
        else:
            response = get_parameter()
            print(f"[Device parameters]: ", response.json())

@client_io.on("DeviceChanged")
def DeviceChanged_Handler(Notice):
    print(f"[NOTIFICATION FROM THE SERVER]: {Notice}")

@client_io.event
def disconnect():
    print("Disconnected to the Server")

host = input("Enter Server IP_Address: ")
port = input("Enter Server PORT: ")
client_io.connect(f"http://{host}:{port}")
