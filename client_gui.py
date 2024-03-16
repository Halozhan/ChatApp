import tkinter
import socket
from threading import Thread


def send(event=None):
    msg = input_message.get()
    input_message.set("")
    client_socket.send(msg.encode())
    if msg == "exit":
        client_socket.close()
        window.quit()


def receive_message(socket):
    while True:
        message = socket.recv(1024).decode()
        chat_history.insert(tkinter.END, message)


def on_delete(event=None):
    input_message.set("exit")
    send()


window = tkinter.Tk()
window.title("Chat Client")

frame = tkinter.Frame(window)
scrollbar = tkinter.Scrollbar(frame)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
chat_history = tkinter.Listbox(frame, height=15, width=50, yscrollcommand=scrollbar.set)
chat_history.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
frame.pack()
input_message = tkinter.StringVar()
input_box = tkinter.Entry(window, textvariable=input_message)

input_box.bind("<Return>", send)
input_box.pack(side=tkinter.LEFT,  fill=tkinter.BOTH, expand=tkinter.YES, padx=5, pady=5)
send_button = tkinter.Button(window, text="전송", command=send)
send_button.pack(side=tkinter.RIGHT, fill=tkinter.X, padx=5, pady=5)


ADDRESS = "localhost"
PORT = 14949

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ADDRESS, PORT))

thread = Thread(target=receive_message, args=(client_socket,))
thread.daemon = True
thread.start()

window.protocol("WM_DELETE_WINDOW", on_delete)

window.mainloop()
