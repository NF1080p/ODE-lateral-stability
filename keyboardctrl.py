from pynput import keyboard
import time
bank = 0
pitch = 0
ap_on = 0
set_angle = 0
def on_press(key, injected):
    global bank, pitch, ap_on
    try:
        if key.char == 'a':
            bank -= 1
            time.sleep(0.05)
        elif key.char == 'd':
            bank += 1
            time.sleep(0.05)
        elif key.char == 'w':
            pitch += 1
            time.sleep(0.05)
        elif key.char == 's':
            pitch -= 1
            time.sleep(0.05)
        elif key.char == 'p':
            ap_on = 1 - ap_on
            print('Autopilot toggled to {}'.format(ap_on))
            time.sleep(0.05)

    except AttributeError:
        print('special key {} pressed'.format(
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

while True:
    print(bank, pitch)
    time.sleep(0.05)