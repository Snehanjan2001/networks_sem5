import random
import socket
import threading
import time

server = socket.socket()
port = 12349
server.bind(('localhost', port))
server.listen(5)
connection = True


def inject_error(msg):
    prob = random.randint(0, 9)
    if (prob <= 4):
        ch = msg[0:1]
        if ch == '1':
            ch = '0'
        else:
            ch = '1'
        msg = ch + msg[1::]

    return msg


def handle_connection(sender, reciever):
    msg = sender.recv(1024).decode()
    while msg != "exit":
        msg = inject_error(msg)
        print(msg)
        time.sleep(random.randint(0, 2))
        reciever.sendall(f'{msg}'.encode())
        acknowledgement = reciever.recv(1024)
        print(f"Recieved {acknowledgement.decode()}")
        sender.sendall(acknowledgement)
        print("Ack sent")
        msg = sender.recv(1024).decode()

    reciever.send(msg.encode())
    print("Done")
    sender.close()
    reciever.close()
    server.close()


while connection:
    c, caddr = server.accept()
    print('Got connection from', caddr)
    r, raddr = server.accept()
    print('Got connection from', raddr)

    thread = threading.Thread(target=handle_connection, args=(c, r))
    thread.start()
    print(f"Active Coonections is : {threading.active_count() - 1} ")

server.close()
