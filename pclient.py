import random
import socket

#Create socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",4000))
print('Connect to:', "127.0.0.1,4000")

#Send and recieve messages from client, checking they're correct
try:
    s.send("Hello\r\n".encode())
    greetings = s.recv(80).decode()
    if greetings != "Greetings\r\n":
        s.close()
        print("Greetings not recieved")
    s.send("Game\r\n".encode())
    ready = s.recv(80).decode()
    if ready != "Ready\r\n":
        s.close()
        print("Ready recieved")
except:
    print("Disconnected")

###############################################

try:
    while True:
        #Ask for guess
        guess = input("What is your guess? ")

        #if guess isn't a digit then ask again
        if not guess.isdigit():
            continue

        #Send guess to server
        s.send(("My Guess is: " + guess + "\r\n").encode())

        #Recieve distance from value and print out if close, far or correct
        dist = s.recv(80).decode()
        if (dist == "Far\r\n"):
            print("You are way off")
        elif (dist == "Close\r\n"):
            print("You are close")
        elif (dist == "Correct\r\n"):
            print("You guessed correctly!")
            break

    #Close connection
    s.close()
    print('closed')
except:
    s.close()
    print("Closed")
