import socket
from threading import Thread


def receive_message(socket):
    while True:
        message = socket.recv(1024).decode()
        print(message)


# Create a socket object
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the address and port
ADDRESS = "localhost"
PORT = 14949
# Connect to the server
socket.connect((ADDRESS, PORT))

# region Start a thread to receive messages
thread = Thread(target=receive_message, args=(socket,))
thread.daemon = True
thread.start()
# endregion

# region Send messages
while True:
    message = input()
    socket.send(message.encode())
    if message == "exit":
        break
# endregion

# Close the connection
socket.close()
