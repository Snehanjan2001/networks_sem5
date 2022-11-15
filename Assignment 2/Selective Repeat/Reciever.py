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
port = 12352
reciever.connect(('localhost',port))

width = int(reciever.recv(1024).decode())
time.sleep(1)

while True:
    print("===========================================")
    lst =[]
    i=0
    # Getting From Server
    while i<width:
        data = reciever.recv(1024).decode()
        print(f"Recived {data}")
        time.sleep(.5)
        msg = data.split(":")[0]
        index = data.split(":")[1]
        if msg == LRC(msg[1::]):
            lst.append(f"ACK:{index}")
        else:
            lst.append(f"NACK:{index}")
        i=i+1

    print("\nAll messages Recived\n")

    # Sending to Server
    for msg in lst:
        print(f"Sending {msg}")
        reciever.sendall(msg.encode())
        time.sleep(1)
    print("\nAll ackn sent")
    print("===========================================")







    # print("Recieving")
    # msg = reciever.recv(1024).decode()
    # time.sleep(random.randint(0,2))
    # if LRC(msg[1::])==msg:
    #     print(f"Message is :- {msg[1::]}")
    #     reciever.sendall("ACK".encode())
    # else:
    #     print("Incorrect message")
    #     reciever.sendall("NACK".encode())
    # print("===========================================")

reciever.close()