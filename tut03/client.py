import socket
import sys

# Creating a new socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The IP address and port number of the server will be taken as command line arguments. 
# The command line arguments will be taken from the argv list
server_ip = sys.argv[1]
server_port = int(sys.argv[2])

print(f"Connecting to the server {server_ip} port {server_port}...")

# Creating a Fake Client for server1.
# An unexpected behaviour of server1, which should ideally connect to only one client at a time and refuse other clients,
# was connecting to two clients at a time. Hence, we create a fake client, connect it to the server,
# and disconnect it right away. Next, we connect our original client. Since two clients have been connected,
# the issue is solved, and the server works as expected.

client_socket.settimeout(1) # if the client cannot connect for more than 0.5s, then it means that some connection already exists

try:
    client_socket.connect((server_ip, server_port))
except:
    print("Client is already connected, please try after sometime.")
    exit(1)
else:
    client_socket.close()

# Original client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(1)
try:
    client_socket.connect((server_ip, server_port))
except:
    print("A client is already connected, please try after sometime.")
    exit(1)

print("\nConnection established.")
client_socket.settimeout(None)
# The client will keep on the sending and receiving messages as long as the client does not wish to continue, and breaks
while True:
    print("\nEnter the message to send to the server: ", end="")

    # Taking input - the message to send to the server
    str = input()
    client_socket.sendall(bytes(str, "utf-8"))

    # Receving reply from the server in bytes and decoding it to a string
    msg = client_socket.recv(1024)
    msg = msg.decode()
    print(f"\nServer replied: {msg}")

    # Asking if the client wishes to continue. If yes, repeat the above process. Otherwise, break.
    print("Do you wish to continue? (Y/N) : ", end="")
    str = input()

    # Making sure the client gives appropriate input
    while str != 'N' and str != 'Y':
        print("Invalid input. Answer using Y or N only.")
        print("Do you wish to continue? (Y/N) : ", end="")
        str = input()

    if str == 'N':
        break

print("\nClosing the connection")
client_socket.close()
