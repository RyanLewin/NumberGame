import random
import socket

#Create socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",4001))
print('Connect to:', "127.0.0.1,4001")
#Send hello and check that receive is Admin-Greetings
s.send("Hello\r\n".encode())
greetings = s.recv(80).decode()
if greetings != "Admin-Greetings\r\n":
    s.close()
    print("Admin-Greetings not recieved")
#Send who command to server
s.send("Who\r\n".encode())

#Recieve string of players and if string is too many bytes,
#split it into fragments
players = ""
while True:
    fragments = s.recv(4096).decode()
    if fragments:
        players += str(fragments)
    else:
        break

#print string and then close connection
print(players)
s.close()
