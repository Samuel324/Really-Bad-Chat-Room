import socket
import threading

#checks to see if the username is 'admin' if it is, the client gets admin powers :), if not then they don't :(
nickname = input("Choose Your Nickname:")
if nickname == 'admin':
    password = input("Enter Password for Admin:")

    
 #creates a client to connect to the server with, using the imported socket module
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect to a host
client.connect(('192.168.87.22',5555))

stop_thread = False

#checks to see if the client is still connected to the server, if it isn't then it is removed from the server
#also checks to see if the clients wants to be a admin, if it does want to be then they get to put in the password, if it is wrong then no admin privilages.
#thirdly, checks to see if the username the client inputs is bannned, not useful for banning people as they can reopen and choose a different name, better suited towards
#the banning of hate speach as a username
def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break    
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection is Refused !! Wrong Password")
                        stop_thread = True
                # Clients those are banned can't reconnect
                elif next_message == 'BAN':
                    print('Connection Refused due to Ban')
                    client.close()
                    stop_thread = True
            else:
                print(message)
#if the user fails to connect to the server it displays this message.             
        except:
            print('Error Occured while Connecting')
            client.close()
            break

#how the client is able to send information (messages) to the server, along with to other users who are also connected to the server.
def write():
    while True:
        if stop_thread:
            break
        #Getting Messages
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    # 2 for : and whitespace and 6 for /KICK_
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    # 2 for : and whitespace and 5 for /BAN
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
            else:
                print("Commands can be executed by Admins only !!")
        else:
            client.send(message.encode('ascii'))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
