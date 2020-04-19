from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time

class Client:
    """
    for communication with server
    """
    HOST = "localhost"
    PORT = 5050
    ADDR = (HOST, PORT)
    BUFSIZ = 512
    FORMAT = "utf8"

    def __init__(self, name):
        """
        Init object and send name to server
        :param name: str
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name + ": ")
        self.lock = Lock()


    def receive_messages(self):
        """
        Receive messages from the server
        :return: None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode(self.FORMAT)
                self.lock.acquire()     # the lock prevents the threads from accessing the same memory space
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCEPTION]", e)
                break


    def send_message(self, msg):
        """
        Send messages to the server
        :param msg: str
        :return: None
        """
        try:
            self.client_socket.send(bytes(msg, self.FORMAT))
            if msg == "{quit}":
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print("[EXCEPTION]", e)

    
    def get_messages(self):
        """
        Returns a list of strings
        :return: list[str]
        """
        messages_copy = self.messages[:]     # copy of the messages list
        
        # make sure memory is safe to access from the thread
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy

    def disconnect(self):
        self.send_message("{quit}")