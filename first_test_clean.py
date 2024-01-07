import time

import cv2
import numpy as np
import pyautogui
from PIL import Image, ImageChops


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
            # Target is above
            print('Target is below')
        elif deviation[1] < -5:
            # Target is below
            print('Target is above')
    elif abs(deviation[0]) > 5:
        # Target is not horizontally centered
        if deviation[0] > 5:
            # Target is to the right
            print('Target is to the right')
        elif deviation[0] < -5:
            # Target is to the left
            print('Target is to the left')
    elif abs(deviation[0]) < 5 and abs(deviation[1]) < 5:
        # Target is centered
        print('Target is centered')
        check_centered()
    
    print(deviation)

def check_centered():
    """
    Checks if the target is centered or anticentered
    """
    #finds average brightness of the center of the found compass
    corners = [(30,30),(39,30),(30,39),(39,39)]
    found_compass = Image.open('pictures/found_compass.png')
    gs_compass = found_compass.convert('L')
    brightness = []
    #average every pixel in the square cornered by corners
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
    while True:
        time.sleep(1)
        # screen_shot()
        # mono_color()
        find_compass()
        dev = target_deviation()
        output(dev)
        #check_centered()
