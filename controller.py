#uses pyvJoy to simulate an xbox controller to control the game

import vgamepad as vg
import time

#sets up the controller
gamepad = vg.VX360Gamepad()

def tap_button(button):
    gamepad.press_button(button)
    gamepad.update()
    time.sleep(0.05)
    gamepad.release_button(button)
    gamepad.update()


a = vg.XUSB_BUTTON.XUSB_GAMEPAD_A
b = vg.XUSB_BUTTON.XUSB_GAMEPAD_B
x = vg.XUSB_BUTTON.XUSB_GAMEPAD_X
y = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y
lb = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
rb = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
back = vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
start = vg.XUSB_BUTTON.XUSB_GAMEPAD_START
ls = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
rs = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB
up = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
down = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
left = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
right = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT


time.sleep(1)
tap_button(a)

time.sleep(1)

gamepad.left_joystick_float(0,1)
gamepad.update()

time.sleep(3)

gamepad.left_joystick_float(0,0)
gamepad.update()

