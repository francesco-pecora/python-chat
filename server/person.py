class Person:
    """
    Represents a user of the python chat, holds name, socket client, and IP address
    """
    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self, name):
        self.name = name

    def __repr__(self):
        return f"Person({self.addr}, {self.name})"
        