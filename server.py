import random
import socket
import threading
import select

#Check numbers distance to correct number
def within(conn, value, goal):
    try:
        diff = abs(goal - int(value))
        #return false if less than 3, notify that player is close
        if diff < 3 and diff > 0:
            conn.send(("Close\r\n").encode())
            return False
        #return true if correct
        elif diff == 0:
            conn.send(("Correct\r\n").encode())
            return True
        #return false, notify that player is far
        else:
            conn.send(("Far\r\n").encode())
            return False
    except:
        print("Error in within")

#Get socket for given ip and port
def connection(ip, port):
    TCP_IP = ip
    TCP_PORT = port
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    #listen for 5 players and 1 admin
    if port is 4000:
        s.listen(5)
    else:
        s.listen(1)
    return s

#Main Game functionality
def game(conn, addr, num) :
    score = 0
    #loop through until correct answer is given
    while True:
        try:
            #get guess from user
            guess = conn.recv(80).decode()
            if guess.split(':')[0] != "My Guess is":
                break

            #make sure the string contains a number
            for x in guess.split():
                if x.isdigit():
                    guess = x

            ##Add one to score and convert guess to a number
            guess = float(guess)
            score += 1
            
            # if within returns true then add users address and score to
            #Scores.txt
            if within(conn, guess, num) == True:
                fo = open("Scores.txt", "a")
                scoreText = str(addr), score
                append = str(scoreText)
                fo.write(append + "\n")
                fo.close()
                break
        except:
            print("Error in Game")
            break
        
    conn.close()
    
# Check that the player is valid through each check
def check_player (conn,clients,r) :
    print('Connection address from:', r)
    try:
        #Check for initial hello message
        helloMsg = conn.recv(80).decode()
        if helloMsg != "Hello\r\n":
            conn.close()
            print("Hello not recieved")

        #if address port is 4000 (client) then send and check for client messages
        if r[1] == 4000:
            conn.send("Greetings\r\n".encode())
            gameMsg = conn.recv(80).decode()
            if gameMsg != "Game\r\n":
                s.close()
                print("Game not recieved")
            conn.send("Ready\r\n".encode())

            #Get a random number between 1 and 30
            num = random.randrange(1, 30)
            #Call game function
            game(conn, r, num)

            #if the connection is in the clients list, remove them
            if conn in clients:
                clients.remove(conn)
    except:
        conn.close()
        #if the connection is in the clients list, remove them
        if conn in clients:
            clients.remove(conn)
        
    print(r, "closed")

#Check that the admin is valid and send players list
def check_admin (conn,clients,r) :
    try:
        #Check for initial hello message
        helloMsg = conn.recv(80).decode()
        if helloMsg != "Hello\r\n":
            conn.close()
            print("Hello not recieved")
            
        conn.send("Admin-Greetings\r\n".encode())
        who = conn.recv(80).decode()
        if who != "Who\r\n":
            conn.close()
            print("Who not recieved")

        #create string of each player in the client list seperated by
        # a new line and send to the admin client
        sendToAdmin = "Number of players: " + str(len(clients)) + ".\n They are: \n"
        for client in clients:
            sendToAdmin += str(client.getsockname()) + "\n"
        sendToAdmin += "\r\n"
        conn.send(sendToAdmin.encode())

        #close connection
        conn.close()
        print(r, " closed")
    except:
        print("Removed", r)
        conn.close()
        

####################################################
#Set IP
ip = "127.0.0.1"
#Set port and socket for client 
port = 4000
player = connection(ip, port)
#Set port and socket for admin
port = 4001
admin = connection(ip, port)

#Add player and admin socket to list
inputs = [player, admin]
#Create list of clients
clients=[]


while True:
    #Select inputs and add to the read array
    (read, write, excep) = select.select(inputs, [], [])

    ## loop through all clients in the read array
    for r in read:
        #if r is a player or admin socket then try and accept, append them to
        #the clients list and start a thread
        if r is player or admin:
            try:
                (conn, addr) = r.accept()
            except:
                print("Accept error")

            try:
                if r is player:
                    clients.append(conn)
                    t = threading.Thread(target = check_player, args = (conn,clients,r.getsockname()))
                else:
                    t = threading.Thread(target = check_admin, args = (conn,clients,r.getsockname()))
                
                t.start()
            #Exception if thread fails
            except:
                print("Thread error")

            
