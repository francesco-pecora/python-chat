from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5050
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512
FORMAT = "utf8"

# GLOBAL VARIABLES
persons = []

# creating internet socket
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def broadcast(msg, name):
    """
    Send welcome message to all clients
    :param msg: bytes["uft8"]
    :param name: str
    :return: None
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, FORMAT) + msg)
        except Exception as e:
            print("[EXCEPTION]", e)


def client_communication(person):
    """
    Thread to handle messages from client
    :param person: Person
    :return:
    """
    client = person.client

    # first message received is always the persons name
    name = client.recv(BUFSIZ).decode(FORMAT)
    person.set_name(name)

    msg = bytes(f"{name} has joined the chat!", FORMAT)
    broadcast(msg, "")

    while True:
        try:
            msg = client.recv(BUFSIZ)
            if msg == bytes("{quit}", FORMAT):      # if message is {quit} disconnect client
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", FORMAT), "")
                print(f"[DISCONNECTED] {name} disconnected ")
                break
            else:                                   # send messages to every other client
                broadcast(msg, name)
                print(f"{name}: ", msg.decode(FORMAT))
                
        except Exception as e:
            print("[EXCEPTION]", e)


def wait_for_connection():
    """
    Waiting for connection from new client, and start new thread once connected
    :param SERVER: SOCKET
    :return: None
    """
    while True:
        try:
            client, addr = SERVER.accept()          # wait for a new connection
            person = Person(addr, client)
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break

    print("[CRASHED] Server crashed...")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)                  # open server to listen for connections
    print("[WAITING] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

