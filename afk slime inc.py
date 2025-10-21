from pynput.keyboard import Controller, Listener, KeyCode
import threading
import time

keyboard = Controller()
holding_w = False  # toggle state

def hold_w():
    global holding_w
    while True:
        if holding_w:
            keyboard.press("d")
            time.sleep(1)
            keyboard.release("d")  
        else:
            keyboard.release("w")
            time.sleep(0.1)

thread = threading.Thread(target=hold_w)
thread.daemon = True
thread.start()

def on_press(key):
    global holding_w
    if hasattr(key, "char") and key.char.lower() == "l":
        holding_w = not holding_w
        print("Started holding W" if holding_w else "Stopped holding W")

def on_release(key):
    if key == KeyCode.from_char('\x1b'):  # ESC key
        if holding_w:
            keyboard.release("w")
        print("Exiting...")
        return False

# Start listener
with Listener(on_press=on_press, on_release=on_release) as listener:
    print("Press 'L' to toggle holding W. Press ESC to quit.")
    listener.join()