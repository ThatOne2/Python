#https://pythontic.com/modules/socket/send
import socket
import random
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

clientSocket.connect(("127.0.0.1", "127.0.0.1"))

g = 666 
p_g = 6661 
h = 444
p_h = 4441

def clientSend(s):
    print("Bob (me): " + s)
    clientSocket.send(s.encode())

def clientReceive():
    dataFromServer = clientSocket.recv(1024)
    print("Alice: " + dataFromServer.decode())
    return dataFromServer.decode()

def commit(m, r):
        c = ((g ** m) % p_g) * ((h ** r) % p_h)
        return c

# Hello
clientReceive()
clientSend("Hello Alice")

# Bob receives commitment and sends his pick to Alice 
c_alice = int(clientReceive())
r = random.randint(1,6)
clientSend(str(r))

# Bob receives Alice's opening (a, r)
m_alice = int(clientReceive())
r_alice = int(clientReceive())
c_check = commit(m_alice, r_alice)
result = c_check==c_alice
#TODO handle if result false
clientSend("Hey Alice, your opener matches: " + str(result))

#Bob receives final dice roll
clientReceive()