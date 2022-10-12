#https://pythontic.com/modules/socket/send
import socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

clientSocket.connect(("127.0.0.1", 9090))



def clientSend(s):
    data = s
    clientSocket.send(data.encode())

def clientReceive():
    dataFromServer = clientSocket.recv(1024)
    print(dataFromServer.decode())

clientSend("Hello server")
clientReceive()
clientSend("Server, how are you")