import time

import cv2
import numpy as np
import pyautogui
from PIL import Image, ImageChops

import vgamepad as vg

def tap_button(button):
    """
    Presses a button on the controller
    
    Args:
        button (vg.XUSB_BUTTON): Button to press
    """
    gamepad.press_button(button)
    gamepad.update()
    time.sleep(0.05)
    gamepad.release_button(button)
    gamepad.update()

def set_up_controller():
    """
    Sets up the controller buttons as global variables
    """
    
    global a, b, x, y, lb, rb, back, start, ls, rs, up, down, left, right, gamepad
    gamepad = vg.VX360Gamepad()
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


def screen_shot() -> Image:
    """
    Takes a screenshot and saves it to elite_dangerous_bot
    
    Returns:
        Image: Screenshot
    """
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'pictures/screen_shot.png')
    return myScreenshot

def mono_color() -> Image:
    """
    Converts the screenshot to mono color
    
    Returns:
        Image: Monochrome image
    """
    image = Image.open('pictures/screen_shot.png')
    image = image.convert('L')  # Convert to grayscale
    image.save(r'pictures/gray_scale.png')
    image = image.point(lambda x: 0 if x < 100 else 255, '1')  # Threshold for monochrome
    image.save(r'pictures/mono_color.png')
    return image

def find_compass():
    """
    Finds where the compass is on screen, and returns the coordinates of the compass
    """
    compass = Image.open('pictures/compass_sample.png')
    compass_location = pyautogui.locateCenterOnScreen(compass, grayscale=True, confidence=0.7)
    if compass_location is not None:
        print(compass_location)
        bounds = 35
        box = (
            compass_location[0] - bounds,
            compass_location[1] - bounds,
            compass_location[0] + bounds,
            compass_location[1] + bounds
        )
        screen_shot().crop(box).save(r'pictures/found_compass.png')
    else:
        print('Compass not found')
        gamepad.left_joystick_float(0, 0)
        gamepad.update()

def target_deviation() -> tuple:
    """
    Finds the target on the compass, and returns the deviation from center
    
    Returns:
        tuple: Deviation from center
    """
    found_compass = Image.open('pictures/found_compass.png')
    compass_sample = Image.open('pictures/compass_sample.png')
    found_compass = found_compass.convert('RGB')
    compass_sample = compass_sample.convert('RGB')
    solid_difference = ImageChops.difference(found_compass, compass_sample)
    solid_difference.save(r'pictures/solid_difference.png')
    solid_difference = np.array(solid_difference)
    solid_difference = cv2.cvtColor(solid_difference, cv2.COLOR_BGR2GRAY)
    brightest = cv2.minMaxLoc(solid_difference)
    coords = brightest[3]
    deviation = (coords[0] - 35, coords[1] - 35)
    return deviation

def output(deviation: tuple):
    """
    Outputs the deviation and target position
    
    Args:
        deviation (tuple): Deviation from center
    """
    if abs(deviation[0]) < 5 and abs(deviation[1]) > 5:
        # Target is horizontally centered
        if deviation[1] > 5:
            # Target is below, left joystick up
            print('Target is below')
            gamepad.left_joystick_float(0, 0.5)
            gamepad.update()
        elif deviation[1] < -5:
            # Target is above, left joystick down
            print('Target is above')
            gamepad.left_joystick_float(0, -0.5)
    elif abs(deviation[0]) > 5:
        # Target is not horizontally centered
        if deviation[0] > 5:
            # Target is to the right, left joystick right
            print('Target is to the right')
            gamepad.left_joystick_float(0.5, 0)
        elif deviation[0] < -5:
            # Target is to the left, left joystick left
            print('Target is to the left')
            gamepad.left_joystick_float(-0.5, 0)
    elif abs(deviation[0]) < 5 and abs(deviation[1]) < 5:
        # Target is centered
        print('Target is centered')
        gamepad.left_joystick_float(0, 0)
        check_centered()
    gamepad.update()
    print(deviation)

def check_centered():
    """
    Checks if the target is centered or anticentered
    """
    #finds average brightness of the center of the found compass
    found_compass = Image.open('pictures/found_compass.png')
    gs_compass = found_compass.convert('L')
    brightness = []
    #finds average brightness of the center of the found compass
    for x in range(30,40):
        for y in range(30,40):
            brightness.append(gs_compass.getpixel((x,y)))
    avg_brightness = sum(brightness)/len(brightness)
    print(avg_brightness)
    if avg_brightness > 100:
        print('Target is centered')
    elif avg_brightness > 30:
        print('Target is anticentered')
    else:
        print('Target is not centered or anticentered')



if __name__ == '__main__':
    set_up_controller()
    time.sleep(1)
    tap_button(a)
    while True:
        #time.sleep(0.2)
        # screen_shot()
        # mono_color()
        find_compass()
        dev = target_deviation()
        output(dev)
