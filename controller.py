#uses pyvJoy to simulate an xbox controller to control the game

import vgamepad as vg
import time

#sets up the controller
gamepad = vg.VX360Gamepad()
time.sleep(2)

for _ in range(5):
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(0.05)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(1)


#create a wrapper for the buttons on the controller

def tap_button(button):
    gamepad.press_button(button)
    gamepad.update()
    time.sleep(0.05)
    gamepad.release_button(button)
    gamepad.update()

def letter_to_button(letter):
    if letter == 'a':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_A
    elif letter == 'b':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_B
    elif letter == 'x':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_X
    elif letter == 'y':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_Y
    elif letter == 'l':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
    elif letter == 'r':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
    elif letter == 'back':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
    elif letter == 'start':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_START
    elif letter == 'ls':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
    elif letter == 'rs':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
    elif letter == 'up':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
    elif letter == 'down':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
    elif letter == 'left':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
    elif letter == 'right':
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
    else:
        print('invalid button')
        return None

#tests left joystick input
#gamepad.left_joystick(x_value=0, y_value=0)


