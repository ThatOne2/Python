#CODE from: https://www.youtube.com/watch?v=3QiPPX-KeSc
#CODE from: https://gist.github.com/Oborichkin/d8d0c7823fd6db3abeb25f69352a5299 
#CODE from: https://github.com/bopace/generate-primes/blob/master/prime.py 
#CERTIFICATES AND KEYS: https://quaint-larkspur-ffd.notion.site/Creating-certificates-ce19c4acddb04c9a80671d46c2bd78b6
#TLS (SSL) library from: https://docs.python.org/3/library/ssl.html 
#Passwords to all keys and certs are 112233

import random
import socket
import threading
import ssl

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
  
    g, p = setup(conn, addr)
    c = int(server_recive(conn, addr))
    print("[RECIVED COMMIT]")
    #print(f"[ALICE COMMIT] = {c}")
    roll = CalcRoll(g, p, conn, addr)
    if roll != 0: 
        r = int(server_recive(conn, addr))
        a = int(server_recive(conn, addr))
        print(f"[RECIVED] randint {r}, Alice guess {a}")
        if open(g, p, r, a, c): 
            print("[COMMIT ACCEPTED]")
            server_send(conn, addr, "ACCEPTED")
            result(conn, addr, a, roll)
        else: 
            print("[COMMIT NOT ACCEPTED]")
            server_send(conn, addr, "NOT ACCEPTED")

        print("")
    conn.close() 
 
#================== CALC DICE ROLL ====================
def CalcRoll(g, p, conn, addr):
    bR = random.randint(1, 20)
    h = g**bR % p 
    r = generate_prime(5)
    bC = (g**bR)*(h**r) #Bob contribution to the dice roll
    aC = int(server_recive(conn, addr))
    server_send(conn, addr, str(bC))
    aR = int(server_recive(conn, addr))
    ar = int(server_recive(conn, addr))
    server_send(conn, addr, str(bR))
    server_send(conn, addr, str(r))
    if open(g, p, ar, aR, aC):
        isAck = server_recive(conn, addr)
        server_send(conn, addr, "ACK")
        if isAck == "ACK":
            roll = ((aR + bR) % 6) + 1
            print(f"[ROLL WAS]: {roll}")
            return roll
    else:
        isAck = server_recive(conn, addr)
        server_send(conn, addr, "NOT_ACK")
        return 0

#================== RECIVE MESSAGES ====================
def server_recive(conn, addr):
    msg_lenght = conn.recv(HEADER).decode(FORMAT) #Blocking line of code
    connected = True
    if msg_lenght: #Message lenght not null
        msg_lenght = int(msg_lenght)
        msg = conn.recv(msg_lenght).decode(FORMAT) #Actual Message

        return msg


#================== SEND MESSAGES ====================
def server_send(conn, addr, msg):
    conn.send(msg.encode(FORMAT))


#================== CHECK IF NUMBER IS PRIME ====================
def is_prime(num, test_count):
    if num == 1:
        return False
    if test_count >= num:
        test_count = num - 1
    for x in range(test_count):
        val = random.randint(1, num - 1)
        if pow(val, num-1, num) != 1:
            return False
    return True

#================== FIND RANDOM PRIME ====================
def generate_prime(n):
    found_prime = False
    while not found_prime:
        p = random.randint(2**(n-1), 2**n)
        if is_prime(p, 100):
            return p

#================== AGREE UPON G AND P ====================
def setup(conn, addr):
    msg = server_recive(conn, addr)
    if msg == "[ROLL THE DICE!]":
        g = generate_prime(100)
        p = generate_prime(50)
        server_send(conn, addr, str(g))
        server_send(conn, addr, str(p))
        print("[PARAMETERS SETUP]")
        return g, p


#================== OPEN COMMIT ====================
def open(g, p, r, a, c):
    hh = (g**a) % p
    cc = (g**a)*(hh**r)
    return (cc == c)

#================== SEND RESULT ====================
def result(conn, addr, a, d):
    if a == d:
        print("[ALICE GUESSED CORRECT]")
        server_send(conn, addr, "[ALICE GUESSED CORRECT]")
    else:
        print("[ALICE DID NOT GUESS CORRECT]")
        server_send(conn, addr, "[ALICE DID NOT GUESS CORRECT]")


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
if __name__== "__main__":
    print("[SERVER STARTING]...")
    start()

