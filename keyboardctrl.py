from pynput import keyboard
import threading

#Please note: keyboard listener automatically records keyboard inputs but only if typed into the console. Press A to bank left and D to bank right from viewer POV, and P to toggle autopilot.

aileron_input = 0

ap_on = 0

'''Adapted from the function use case given in pynput official documentation https://pypi.org/project/pynput/.
Note: injection refers to a "virtual" key press and is not used here.
Built-in char attribute of key pressed influences global parameters: P changes global ap_on and A and D change global aileron_input.
Error handling for non-alphanumeric key presses without char attribute.
'''
def on_press(key, injected):
    global aileron_input, ap_on
    try:
        if key.char == 'p':
            ap_on = 1 - ap_on
            print('Autopilot toggled to {}'.format(ap_on))
        if ap_on == 0:
            if key.char == 'a':
                if aileron_input < 30:
                    aileron_input += 2

            elif key.char == 'd':
                if aileron_input > -30:
                    aileron_input -= 2

    except AttributeError:
        print('Special key {} pressed'.format(
            key))

def on_release(key, injected):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

'''Collect key press and release events'''

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()


