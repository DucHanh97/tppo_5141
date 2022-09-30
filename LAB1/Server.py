import socket
import threading
from time import sleep
import Device as device

HOST   = "127.0.0.1"
PORT = 55555
SERVER_ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSGAGE = "!DISCONNECT"
clientlist = []

cur_Canvas  = device.getCanvas()
cur_Light   = device.getLightFlow()
cur_Illumin = device.getIllumination()
Dv_Params = {"canvas":cur_Canvas, "lightflow":cur_Light, "illumination":cur_Illumin}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    while True:
        try:
            cmd = conn.recv(20).decode(FORMAT)
            if cmd[0:11] == DISCONNECT_MESSGAGE:
                print(f"Client {addr} disconnected")
                clientlist.remove(conn)
                break
            if cmd == '':
                print(f"Client {addr} disconnected")
                clientlist.remove(conn)
                break
                
            print(cmd)
            buff = cmd.split()
            if buff[0] == "set":
                if int(buff[1]) != Dv_Params["canvas"] or int(buff[2]) != Dv_Params["lightflow"]:
                    device.setParams(buff[1],buff[2])
            elif buff[0] == "setcanvas":
                if int(buff[1]) != Dv_Params["canvas"]:
                    device.setParams(buff[1], str(Dv_Params["lightflow"]))
            elif buff[0] == "setlight":
                if int(buff[1]) != Dv_Params["lightflow"]:
                    device.setParams(str(Dv_Params["canvas"]), buff[1])
            else:
                msg = "canvas="+str(Dv_Params["canvas"])+"; lightflow="+str(Dv_Params["lightflow"])+"; illumination="+str(Dv_Params["illumination"])
                conn.send(msg.encode(FORMAT))
            
        except:
            print(f"Client {addr} disconnected")
            clientlist.remove(conn)
            break

    conn.close()

def handle_send(Dv_Params):
    msg = "canvas="+str(Dv_Params["canvas"])+"; lightflow="+str(Dv_Params["lightflow"])+"; illumination="+str(Dv_Params["illumination"])
    for remote_client in clientlist:
        remote_client.send(msg.encode(FORMAT))

# def handle_cmd(cmd):
#     buff = cmd.split()
#     if buff[0] == "set":
#         if int(buff[1]) != Dv_Params["canvas"] or int(buff[2]) != Dv_Params["lightflow"]:
#             device.setParams(buff[1],buff[2])
#     elif buff[0] == "setcanvas":
#         if int(buff[1]) != Dv_Params["canvas"]:
#             device.setParams(buff[1], str(Dv_Params["lightflow"]))
#     elif buff[0] == "setlight":
#         if int(buff[1]) != Dv_Params["lightflow"]:
#             device.setParams(str(Dv_Params["canvas"]), buff[1])

def send_change_state():
    global Dv_Params
    while True:
        sleep(1)
        cur_Canvas  = device.getCanvas()
        cur_Light   = device.getLightFlow()
        if (cur_Canvas != Dv_Params["canvas"]) or (cur_Light != Dv_Params["lightflow"]):
            device.setParams(str(cur_Canvas), str(cur_Light))
            Dv_Params["canvas"] = device.getCanvas()
            Dv_Params["lightflow"] = device.getLightFlow()
            Dv_Params["illumination"] = device.getIllumination()
            handle_send(Dv_Params)

def start():
    server.listen()
    print(f"[LISTENING] Server is listenning on {HOST}")
    while True:
        conn, addr = server.accept()
        clientlist.append(conn)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()}")
        thread1 = threading.Thread(target=handle_client, args=(conn, addr))
        thread1.start()
        thread2 = threading.Thread(target=send_change_state, args=())
        thread2.start()


print("Server is starting...")
start()



