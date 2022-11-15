import socket
import time

client = socket.socket()
port = 12348
client.connect(('localhost',port))


def LRC(val):
    odd = 0
    for i in val:
        if(i=='1'):
            odd+=1
        
    return str(odd%2)+val


width = int(input("Enter Window Size : "))
lst = []
flag = []
times =[]
cur = 0
prev = cur


# Sending Window size
client.sendall(f"{width}".encode())
time.sleep(1)

# Ading First frames to it
while True:
    msg = input('Enter Binary String : ')
    lst.insert(cur%width,msg)
    flag.insert(cur%width,False)
    times.insert(cur%width,0)
    cur=cur+1
    if cur%width==prev:
        break

cur = 0
# Startiung loop
while True:
    print("===========================================")
    # Send all Binary Strings
    cur_ind = cur
    while True:
    # for i in range(len(lst)):
        i = cur_ind%width
        # if flag[i]==False:
        if lst[i] != "exit":
            msg = f"{LRC(lst[i])}:{i}"
        print(f"Sent {msg}")
        client.sendall(msg.encode())
        times[i]= time.time()
        time.sleep(1)
        cur_ind=cur_ind+1
        if cur_ind%width == cur%width:
            break;

    print("All message Sent")

    # Checking For Acknowledement
    cur_ind = cur
    while True:
    # for i in range(len(lst)):
        i = cur_ind%width
        print(f"Waiting for {i}")
        # if flag[i]==False:
        ack = client.recv(1024).decode()
        index = int(ack.split(":")[1])
        ackval = ack.split(":")[0]
        triptime = time.time()-times[index]
        if triptime < 27:
            if ackval == "NACK":
                flag[index] = False
                print(f"Unsuccesfully, sending again Round Trip Time : {triptime}")
            else :
                flag[index] = True
                print(f"Succesfully Recieved Round Trip Time : {triptime}")
        else:
            print("Timeout Had Expired, Sending Again")
                
        cur_ind=cur_ind+1
        if cur_ind%width == cur%width:
            break;

    print("All Ack Recived")

    # Adding new item to sliding window
    cur_ind = cur
    while True:
    # for i in range(len(lst)):
        i=cur%width
        if flag[i]==True:
            msg = input('Enter Binary String : ')
            lst[i] = msg
            flag[i]=False
        else:
            break
        cur = cur +1
        if cur%width == cur_ind%width  :
            break


client.close()