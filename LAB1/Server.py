from http import server
import socket
import threading
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


