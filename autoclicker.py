from pynput import keyboard, mouse
import threading
import random
import time

# Controller for simulating mouse clicks
mouse_controller = mouse.Controller()

# Flag to track whether 'n' is currently held down
clicking = False
click_thread = None


def click_loop():
    """Runs in a separate thread, clicking with a random delay while 'clicking' is True."""
    while clicking:
        mouse_controller.click(mouse.Button.left)
        time.sleep(random.uniform(0, .01))


def on_press(key):
    global clicking, click_thread

    try:
        if key.char == 'n' and not clicking:
            clicking = True
            click_thread = threading.Thread(target=click_loop, daemon=True)
            click_thread.start()
    except AttributeError:
        # Special keys (ctrl, shift, etc.) don't have .char, ignore them
        pass


def on_release(key):
    global clicking

    try:
        if key.char == 'n':
            clicking = False
    except AttributeError:
        pass

    # Optional: stop the listener with the Esc key
    if key == keyboard.Key.esc:
        return False


print("Listening for 'n' key... Hold it down to autoclick. Press Esc to quit.")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()