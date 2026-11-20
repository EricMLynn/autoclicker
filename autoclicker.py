from pynput import keyboard, mouse
import threading
import random
import time

# Controller for simulating mouse clicks
mouse_controller = mouse.Controller()

# Flag to track whether autoclicking is currently active
clicking = False
click_thread = None

# Tracks whether 'n' is currently held down, so we only toggle on release
n_held = False


def click_loop():
    """Runs in a separate thread, clicking with a random delay while 'clicking' is True."""
    while clicking:
        mouse_controller.click(mouse.Button.left)
        time.sleep(random.uniform(0, 0.01))


def on_press(key):
    global n_held

    try:
        if key.char == 'n':
            n_held = True
    except AttributeError:
        pass


def on_release(key):
    global clicking, click_thread, n_held

    try:
        if key.char == 'n' and n_held:
            n_held = False
            clicking = not clicking  # toggle state

            if clicking:
                click_thread = threading.Thread(target=click_loop, daemon=True)
                click_thread.start()
            # if we just turned it off, click_loop's while-loop will exit on its own
    except AttributeError:
        pass

    # Optional: stop the listener with the Esc key
    if key == keyboard.Key.esc:
        return False


print("Press and release 'n' to start autoclicking. Press and release it again to stop. Press Esc to quit.")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
