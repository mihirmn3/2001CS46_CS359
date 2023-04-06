import socket
import sys
from _thread import *

# Creating server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Taking the server IP address and port number as command line arguments
server_ip = sys.argv[1]
server_port = int(sys.argv[2])

# Binding the server socket to listen to the given IP address and port number
server_socket.bind((server_ip, server_port))
server_socket.listen(0)

# Maintaining a count of the number of clients connected
clients_connected = 0

def calc(client_connection, client_address):

    # Using the global clients_connected variable
    global clients_connected
    
    while True:

        # Receiving message from the client
        msg_bytes = client_connection.recv(1024)

        # If the message size is 0, the client has closed the connection
        if msg_bytes == b'':
            clients_connected -= 1
            print(f"Closing the connection of client {client_address}")
            print(f"{clients_connected} clients currently connected\n")
            client_connection.close()
            break
        
       # The message received is in the form of bytes. Decoding it to a string
        msg = msg_bytes.decode()
        print (f"Recived expression {msg} from client {client_address}")
        
        # Calculating the value of the received expression using eval(). Error is it is an invalid expression
        try:
            ans = eval(msg)
        except:
            ans = "ERROR: Invalid expression"
        ans = str(ans)
        print(f"Sending answer {ans} to the client {client_address}\n")

        # Sending the reply to the client, and storing the length of the message sent
        lenth = client_connection.sendall(bytes(ans, "utf-8"))

print(f"Listening on {server_ip} port {server_port}")

while True:
    
    # Waiting to accept a connection from a client. This line blocks the code until a client connection is made
    # After a client connects, a new socket is assigned to this connection (client_conn)
    # The server socket is always reserved to listen for incoming connections
    client_conn, client_addr = server_socket.accept()

    clients_connected += 1 # increasing the count of number of clients by one, after a client has connected
    
    print(f"\nConnected to client {client_addr}")
    print(f"{clients_connected} clients currently connected\n") # Displaying the count of clients connected

    # Starting a new thread for every client connected. 
    # All the clients will thus, access the server in parallel and independent to each other
    start_new_thread(calc, (client_conn, client_addr,))

server_socket.close()
