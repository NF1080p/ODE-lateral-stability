from pynput import keyboard
import threading

#Please note: keyboard listener automatically records keyboard inputs but only if typed into the console. Press A to bank left and D to bank right from viewer POV, and P to toggle autopilot.

aileron_input = 0

ap_on = 0

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



'''# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()'''



# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
print("Keyboard Inputs Active")

