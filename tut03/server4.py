import socket
import sys
import queue
import select

# Creating server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The socket will not block the code, and hence the operations of all the connected clients
# will go on without interruption. Even if the server is listening for or accepting new connections.
server_socket.setblocking(0)

# Taking the server IP address and port number as command line arguments
server_ip = sys.argv[1]
server_port = int(sys.argv[2])

# Binding the server socket to listen to the given IP address and port number
server_socket.bind((server_ip, server_port))
server_socket.listen(0)
print(f"Listening on {server_ip} port {server_port}")

# Contains a list of all the sockets which can recieve a message. It contains all clients, and the server (since it can also listen)
input_sockets = [server_socket]

# Contains a list of sockets which have messages pending to be sent to their connected clients
output_sockets = []

# Contains a dictionary, which maintains message queues for each socket.
# The queues contain the messages which are to be sent to the client
socket_msgs = {}

# Maintains a count of the number of clients connected
clients_connected = 0

# In each iteration, the server will perform some operations. It will send data to some clients, receive data
# from some clients and close the connections of some. Now, which operation to perform on which client is 
# decided by the select module. It provides asynchronous I/O on multiple file descriptors
while input_sockets:
    
    # Select takes input, the sockets to which clients are connected, the input and output sockets separately
    # It will return 3 lists: 
    # 1. The sockets to read from - We will receive data from the client connected to this socket
    # 2. The sockets to write to - We will send data from the socket mesasge queue to the client connected
    # 3. The sockets which gave an error - Close the connection
    read_sockets, write_sockets, err_sockets = select.select(input_sockets, output_sockets, input_sockets)
    
    # Receiving data from the sockets in the Read list
    for sckt in read_sockets:

        # If socket is the server socket, then reading it means listening for new connections and accepting it
        if sckt is server_socket:
            client_conn, client_addr = server_socket.accept()
            clients_connected += 1
            print(f"\nConnected to client {client_addr}")
            print(f"{clients_connected} clients currently connected\n")

            input_sockets.append(client_conn) # adding the cilent to input list
            socket_msgs[client_conn] = queue.Queue() # creating its message queue

        # If not server socket, then it is a client socket which has data to be received
        else:
            msg_bytes = sckt.recv(1024)
            
            # If data is 0, the client has closed the connection. We remove the client from all the lists
            if msg_bytes == b'':
                client_addr = sckt.getpeername() # Getting the IP address and port of the client
                print(f"Closing the connection of client {client_addr}")
                if sckt in output_sockets:
                    output_sockets.remove(sckt)
                input_sockets.remove(sckt)
                del socket_msgs[sckt]
                sckt.close()
                clients_connected -= 1
                print(f"{clients_connected} clients currently connected\n")

            # If data is not 0, then decode the message, which is in bytes, to string
            else:
                msg = msg_bytes.decode()
                client_addr = sckt.getpeername()
                print (f"Recived expression '{msg}' from client {client_addr}")

                # Echoing the message received from the client, back to the client 
                ans = str(msg)

                # Put the message in the socket's message queue
                socket_msgs[sckt].put(ans)
                
                # Put the socket in output list, since it has a message to be sent
                if sckt not in output_sockets:
                    output_sockets.append(sckt)

    # For sockets to be written, extract the mesasge from message queue and send it
    for sckt in write_sockets:
        try:
            ans = socket_msgs[sckt].get_nowait()
        
        # If nothing in message queue, remove the socket from output list, since it contains nothing to be sent anymore
        except queue.Empty:
            output_sockets.remove(sckt)
        else:
            sckt.sendall(bytes(ans, "utf-8"))
            client_addr = sckt.getpeername()
            print(f"Sending answer '{ans}' to client {client_addr}\n")

    # For sockets which encountered error, we remove them from all the lists and close the connection
    for sckt in err_sockets:
        client_addr = sckt.getpeername()
        print(f"Error encountered. Closing the connection of client {client_addr}")
        input_sockets.remove(sckt)
        if sckt in output_sockets:
            output_sockets.remove(sckt)
        del socket_msgs[sckt]
        sckt.close()
        clients_connected -= 1
        print(f"{clients_connected} clients currently connected\n")

server_socket.close()

# Reference: http://pymotw.com/2/select/
