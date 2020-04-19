from client import Client
from threading import Thread
import time


c1 = Client("Francesco")

def update_messages():
    """
    Display the local list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)                    # update every 1/10 of a second
        new_messages = c1.get_messages()
        msgs.extend(new_messages)

        for msg in new_messages:           # display new messages
            print(msg)

            if msg == "{quit}":
                run = False
                break

Thread(target=update_messages).start()

c1.send_message("Hello Barbara")


c1.disconnect()
