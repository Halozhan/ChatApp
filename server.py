import socket

# Create a socket object
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the address and port
ADDRESS = "localhost"
PORT = 14949
# Connect to the server
socket.bind((ADDRESS, PORT))

# Listen for incoming connections
socket.listen()

# Accept the connection
client_socket, address = socket.accept()

# Receive the message
message = client_socket.recv(1024)
print(message.decode("utf-8"))

# Close the connection
client_socket.close()

# Close the socket
socket.close()
