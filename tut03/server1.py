import socket
import sys

# Creating server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Taking the server IP address and port number as command line arguments
server_ip = sys.argv[1]
server_port = int(sys.argv[2])

# Binding the server socket to listen to the given IP address and port number
server_socket.bind((server_ip, server_port))
server_socket.listen(0)

# The server will always keep running (as it realistically should), unless force quit using Ctrl+C
while True:

    print(f"\nListening on {server_ip} port {server_port}. Waiting for a connection...")

    # Waiting to accept a connection from a client. This line blocks the code until a client connection is made
    # After a client connects, a new socket is assigned to this connection (client_conn)
    # The server socket is always reserved to listen for incoming connections
    client_conn, client_addr = server_socket.accept()

    print(f"\nConnected to client {client_addr}\n")

    while True:
        
        # Receiving message from the client
        msg_bytes = client_conn.recv(1024)

        # If the client closes the connection using conn.close(), the message received has 0 bytes
        if msg_bytes == b'':
            print("Closing the connection\n")
            client_conn.close()
            break

        # The message received is in the form of bytes. Decoding it to a string
        msg = msg_bytes.decode()
        print (f"Recived expression {msg} from client")
        
        # Calculating the value of the received expression using eval(). Error is it is an invalid expression
        try:
            ans = eval(msg)
        except:
            ans = "ERROR: Invalid expression"
        ans = str(ans)
        print(f"Sending answer {ans} to the client\n")

        # Sending the reply to the client, and storing the length of the message sent
        lenth = client_conn.sendall(bytes(ans, "utf-8"))

server_socket.close()
