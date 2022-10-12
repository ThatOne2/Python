import socket
import ssl

#================== CONSTANTS ====================
HEADER = 64
PORT = 9090
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "CLOSE"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

#================== SERVER CONNECTION ====================
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Finnish
client = ssl.wrap_socket(client, keyfile="./CA/client.key", certfile="./CA/client.crt")
client.connect(ADDR)

#================== SEND MESSAGE ====================
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_lenght = str(msg_length).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)


#================== RECIVE MESSAGE ====================
def receive():
    dataFromServer = client.recv(1024)
    print(dataFromServer.decode())


#================== MAIN ====================
send("Hello World!")
receive()
send(DISCONNECT_MESSAGE)