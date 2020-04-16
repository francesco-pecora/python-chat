from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# GLOBAL CONSTANTS
HOST = "localhost"
PORT = 5050
ADDR = (HOST, PORT)
BUFSIZ = 512
FORMAT = "utf8"

# GLOBAL VARIABLES
messages = []

# creating internet socket
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


def receive_messages():
    """
    Receive messages from the server
    :return: None
    """
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode(FORMAT)
            messages.append(msg)
            print(msg)
        except Exception as e:
            print("[EXCEPTION]", e)
            break


def send_message(msg):
    """
    Send messages to the server
    :param msg: str
    :return: None
    """
    client_socket.send(bytes(msg, FORMAT))
    if msg == "{quit}":
        client_socket.close()


receive_thread = Thread(target=receive_messages)
receive_thread.start()

send_message("Francesco")
send_message("Hello")