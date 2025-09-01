import os
from pynput.keyboard import Listener

keys = []
count = 0



def on_press(key):
    global keys, count

    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        keys = []




with Listener(on_press=on_press) as listener:
    listener.join()

