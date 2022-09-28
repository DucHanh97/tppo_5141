from ast import Break
from concurrent.futures import thread
from email import message
from http import client, server
import socket
import threading

PORT = 55555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
print(ADDR)
FORMAT = 'utf-8'
DISCONNECT_MESSGAGE = "!DISCONNECT"
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        try:
            msg = conn.recv(30).decode(FORMAT)
            if msg[12:23] == DISCONNECT_MESSGAGE:
                print(f"Client {addr} disconnected")
                clients.remove(conn)
                break

            print(f"[{addr}] {msg}")
            print(len(msg))
    #        conn.send(msg.encode(FORMAT))
            for remote_client in clients:
                if remote_client != conn:
                    remote_client.send(msg.encode(FORMAT))
        except:                                              #exception handle
            print(f"Client {addr} disconnected")
            clients.remove(conn)
            break

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listenning on {SERVER}")
    while True:
        conn, addr = server.accept()            #Waiting for all clients
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()}")
        clients.append(conn)     #(conn,addr)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("[STARTING] server is starting...")
start()