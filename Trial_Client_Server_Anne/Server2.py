#https://pythontic.com/modules/socket/send
import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind(("127.0.0.1",9090))
serverSocket.listen()

def serverReceive():
    dataFromClient = clientConnected.recv(1024)
    print(dataFromClient.decode()) #Decode from byte to string for printing

def serverSend(s):
    clientConnected.send(s.encode()) #Encode from string to byte for sending



while(True):

    (clientConnected, clientAddress) = serverSocket.accept();

    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]));

    #Message flow, send and receive step-bt-step
    serverReceive()
    serverSend("Hello client")
    serverReceive()