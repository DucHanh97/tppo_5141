import socket
import threading
import Device as device
import xml.etree.ElementTree as ET
import os

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
            xml_data = conn.recv(80).decode(FORMAT)
            print(xml_data)
            root = ET.fromstring(xml_data)
            if root[0].text == DISCONNECT_MESSGAGE:
                print(f"Client {addr} disconnected")
                clientlist.remove(conn)
                break

            if root[0].text == "set":
                if int(root[1].text) != Dv_Params["canvas"] or int(root[2].text) != Dv_Params["lightflow"]:
                    device.setParams(root[1].text,root[2].text)
            elif root[0].text == "setcanvas":
                if int(root[1].text) != Dv_Params["canvas"]:
                    device.setParams(root[1].text, str(Dv_Params["lightflow"]))
            elif root[0].text == "setlight":
                if int(root[2].text) != Dv_Params["lightflow"]:
                    device.setParams(str(Dv_Params["canvas"]), root[2].text)
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

def send_change_state():
    global Dv_Params
    time_cache = os.stat("Device.txt").st_mtime
    while True:
        time_change = os.stat("Device.txt").st_mtime
        if time_change != time_cache:
            time_cache = time_change
            print("File has changed")
            cur_Canvas  = device.getCanvas()
            cur_Light   = device.getLightFlow()

            if cur_Canvas != Dv_Params["canvas"] or cur_Light != Dv_Params["lightflow"]:
                device.setParams(str(cur_Canvas), str(cur_Light))
                Dv_Params["canvas"] = device.getCanvas()
                Dv_Params["lightflow"] = device.getLightFlow()
                Dv_Params["illumination"] = device.getIllumination()
                handle_send(Dv_Params)
                print("Sent data to clients")

def start():
    server.listen()
    print(f"[LISTENING] Server is listenning on {HOST}")
    while True:
        conn, addr = server.accept()
        clientlist.append(conn)
        print(f"[ACTIVE CONNECTIONS] = {threading.active_count()//2+1}")
        for cl in clientlist:
            print(cl)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

print("Server is starting...")

thread = threading.Thread(target=send_change_state, args=())
thread.start()

start()



