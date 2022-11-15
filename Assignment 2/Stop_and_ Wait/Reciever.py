import socket
import time
import random

def LRC(val):
    odd = 0
    for i in val:
        if(i=='1'):
            odd+=1
        
    return str(odd%2)+val


reciever = socket.socket()
port = 12349
reciever.connect(('localhost',port))

msg = ""
while msg != "exit":
    print("===========================================")
    print("Recieving")
    msg = reciever.recv(1024).decode()
    time.sleep(random.randint(0,2))
    if LRC(msg[1::])==msg:
        print(f"Message is :- {msg[1::]}")
        reciever.sendall("ACK".encode())
    else:
        print("Incorrect message")
        reciever.sendall("NACK".encode())
    print("===========================================")

reciever.close()