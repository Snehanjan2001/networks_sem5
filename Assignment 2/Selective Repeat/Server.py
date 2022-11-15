import socket
import threading
import random
import time
from sys import exit

server = socket.socket()
port = 12352
server.bind(('localhost',port))
server.listen(5)
connection = True

def inject_error(msg):
    prob = random.randint(0,9)
    if(prob<=3):
        ch = msg[0:1]
        if ch == '1':
            ch='0'
        else:
            ch='1'
        msg = ch + msg[1::]
    
    return msg


def handle_connection(sender,reciever,width):

    print("===============================================")
    while True:
        lst = []
        # Getting from Sender
        i=0
        while i<width:
            msg = sender.recv(1024).decode()
            if msg == "exit":
                sender.close()
                reciever.close()
                server.close()
                exit()
            print(f"Recieved {msg}")
            lst.append(msg)
            i=i+1
        
        print("\nAll msg recieved\n")

        # Sending all to reciever
        for data in lst:
            msg = data.split(":")[0]
            ind = data.split(":")[1]
            msg = inject_error(msg)
            data = f"{msg}:{ind}"
            reciever.sendall(data.encode())
            time.sleep(1)
            print(f"{data} is sent")

        print("\nAll msg Send\n")

        lst = []
        i=0
        # Getting from Reciever
        while i<width:
            msg = reciever.recv(1024).decode()
            print(f"{msg} recived")
            time.sleep(.5)
            lst.append(msg)
            i=i+1

        print("\nAll ack recieved\n")
            
        # Sending acknowledgement to Sender
        for msg in lst:
            print(f"{msg} is sent to client")
            sender.sendall(msg.encode())
            time.sleep(1)

        print("\nAll message recieved")
        print("===============================================")
    



while connection:
    c,caddr = server.accept()
    print ('Got connection from', caddr )
    r,raddr = server.accept()
    print ('Got connection from', raddr )
    width = int(c.recv(1024).decode())
    r.sendall(f"{width}".encode())

    thread = threading.Thread(target=handle_connection,args=(c,r,width))
    thread.start()
    print(f"Active Coonections is : {threading.active_count()-1} ")

server.close()