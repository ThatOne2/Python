import socket
import ssl
import random
import sys

# ================== CONSTANTS ====================
HEADER = 64
PORT = 9090
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "CLOSE"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)


# ================== CHECK IF NUMBER IS PRIME ====================
def is_prime(num, test_count):
    if num == 1:
        return False
    if test_count >= num:
        test_count = num - 1
    for x in range(test_count):
        val = random.randint(1, num - 1)
        if pow(val, num - 1, num) != 1:
            return False
    return True


# ================== FIND RANDOM PRIME ====================
def generate_prime(n):
    found_prime = False
    while not found_prime:
        p = random.randint(2 ** (n - 1), 2 ** n)
        if is_prime(p, 100):
            return p


# ================== SERVER CONNECTION ====================
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client = ssl.wrap_socket(client, keyfile="./CA/client.key", certfile="./CA/client.crt")
client.connect(ADDR)


# ================== SEND MESSAGE ====================
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_lenght = str(msg_length).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)


# ================== RECIVE MESSAGE ====================
def receive():
    dataFromServer = client.recv(1024)
    msg = dataFromServer.decode()
    return msg


# ================== AGREE UPON G AND P ====================
def setup():
    send("[ROLL THE DICE!]")
    g = int(receive())
    p = int(receive())
    print("[SETUP COMPLETE]")
    return g, p


# ================== COMMIT TO GUESS ====================
def commit(g, p):
    a = random.randint(1, 6)
    print(f"[ALICE GUESS] = {a}")
    h = g ** a % p
    r = generate_prime(10)
    c = (g ** a) * (h ** r)
    # print(f"[ALICE COMMITED] = {c}")
    send(str(c))
    return r, a


# ================== SEND RANDOM INT AND ACTUAL GUESS ====================
def open(r, a):
    send(str(r))
    send(str(a))


# ================== CALC DICE ROLL ====================
def CalcRoll(g, p):
    aR = random.randint(1, 20)
    h = g ** aR % p
    r = generate_prime(5)
    aC = (g ** aR) * (h ** r)  # Alice contribution to the dice roll
    send(str(aC))
    bC = int(receive())
    send(str(aR))
    send(str(r))
    bR = int(receive())
    br = int(receive())
    print("[1]")
    if opencommit(g, p, br, bR, bC):
        print("[2]")
        send("ACK")
        print("[3]")
        isAck = receive()
        print("[4]")
        if isAck == "ACK":
            roll = ((aR + bR) % 6) + 1
            print(f"ROLL WAS: {roll}")
            return roll
    else:
        send("NOT_ACK")
        isAck = receive()
        return 0


# ================== OPEN COMMIT ====================
def opencommit(g, p, br, bR, bC):
    print("[1a]")
    bH = (g ** bR) % p
    print("[2a]")
    bc = (g ** bR) * (bH ** br)
    print("[3a]")
    return (bc == bC)


# ================== MAIN ====================
if __name__ == "__main__":
    g, p = setup()
    r, a = commit(g, p)
    roll = CalcRoll(g, p)
    if roll == 0:
        print("[ERROR IN ROLLING DICE]")
        sys.exit()
    open(r, a)
    ack = receive()
    if ack == "ACCEPTED":
        print("[COMMIT ACCEPTED]")
        print(f"{receive()}")

    else:
        print("[COMMIT NOT ACCEPTED]")
