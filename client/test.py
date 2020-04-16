from client import Client
from threading import Thread
import time


c1 = Client("Francesco")
c2 = Client("Barbara")

def update_messages():
    msgs = []
    run = True
    while run:
        time.sleep(0.1)
        new_messages = c1.get_messages()
        msgs.extend(new_messages)
        for msg in new_messages:
            print(msg)
            if msg == "{quit}":
                run = False
                break

Thread(target=update_messages).start()

c1.send_message("Hello Barbara")
time.sleep(5)
c2.send_message("Hello Francesco")
time.sleep(5)
c1.send_message("How are you?")
time.sleep(5)
c2.send_message("I'm good")
time.sleep(5)

c1.disconnect()
time.sleep(2)
c2.disconnect()