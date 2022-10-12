#https://pythontic.com/modules/socket/send
import socket
import random

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind(("127.0.0.1",9090))
serverSocket.listen()

g = 666 
p_g = 6661 
h = 444
p_h = 4441

def serverReceive():
    dataFromClient = clientConnected.recv(1024)
    print("Bob: " + dataFromClient.decode()) #Decode from byte to string for printing
    return dataFromClient.decode()

def serverSend(s):
    print("Alice (me): " + s)
    clientConnected.send(s.encode()) #Encode from string to byte for sending

    
def commit(m, r):
        c = ((g ** m) % p_g) * ((h ** r) % p_h)
        return c

flag = True

while(flag):

    (clientConnected, clientAddress) = serverSocket.accept();

    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]));

    #Message flow, send and receive step-bt-step
    serverSend("Hello Bob")
    serverReceive()

    # Alice sends first commitment
    r = random.randint(1, 999)
    m = random.randint(1,6) #includes both 1 and 6
    c = commit(m, r)
    serverSend(str(c))

    #Alice receives Bobs pick and sends their opening 
    m_bob = serverReceive()
    serverSend(str(m))
    serverSend(str(r))
    
    #Alice receives Bobs check
    serverReceive()
    
    #TODO handle if check not checks
    #Alice prints the result
    result = ((m + int(m_bob)) % 6) + 1 #Ensures a result between 1 and 6
    serverSend("Dice result: " + str(result))

    flag = False