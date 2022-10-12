#CODE from: https://www.youtube.com/watch?v=3QiPPX-KeSc
#TLS (SSL) library from: https://docs.python.org/3/library/ssl.html 

#Permprase to all keys and certs are 112233
import socket
import threading
import ssl
#To send objects use json or pickle

#================== CONSTANTS ====================
HEADER = 64
PORT = 9090
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "CLOSE"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server = ssl.wrap_socket(
    server, server_side=True, keyfile="./CA/server.key", certfile="./CA/server.crt"
)

server.bind(ADDR)


#================== CLIENT CONNECTION ====================
def handle_client(conn, addr):
    print(f"[CLIENT CONNECTED]: {addr}") 

    connected = True
    while connected: 
        msg_lenght = conn.recv(HEADER).decode(FORMAT) #Blocking line of code
        if msg_lenght: #Message lenght not null
            msg_lenght = int(msg_lenght)
            msg = conn.recv(msg_lenght).decode(FORMAT) #Actual Message
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("[MESSAGE RECIVED]".encode(FORMAT))
    conn.close() 
 


#================== START SERVER ====================
def start():
    server.listen()
    print(f"[SERVER LISTINING] on {SERVER}")
    while True:
        conn, addr = server.accept() #Will wait for at new connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #If we want to see how many are active (minus -1 because it will count start as one thread):
        #print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


#================== MAIN ====================
print("[SERVER STARTING]...")
start()