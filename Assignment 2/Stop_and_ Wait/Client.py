import socket
import time

client = socket.socket()
port = 12349
client.connect(('localhost', port))


def LRC(val):
    odd = 0
    for i in val:
        if (i == '1'):
            odd += 1

    return str(odd % 2) + val


msg = ""
resend = False
while msg != "exit":
    # If Error occurred Send again
    print("===========================================")
    if resend == False:
        msg = input('Enter Binary String\n')
        if msg != "exit":
            msg = LRC(msg)

    # Sending Data
    starttime = time.time()
    client.sendall(msg.encode())
    print(f"Send data {resend}")

    client.settimeout(4)
    # Checking For acknowledgement
    try:
        ack = client.recv(1024).decode()
        endtime = time.time()
        print(f"You Recieved -->  {ack}")
        print(f"Round Trip time {endtime - starttime}")
        if (ack == "NACK"):
            resend = True
        else:
            resend = False
    # Checking for timeout
    except:
        print("Timeout Had Expired, Sending Again")
        resend = True
    client.settimeout(None)
    print("===========================================")

client.close()
