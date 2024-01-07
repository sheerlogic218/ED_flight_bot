#this will be the first proof of concept for the bot
#this will take screen shots of the game convert to mono color, and find the compass and crop accordingly
#it then finds whether the target is solid of hollow and how far away from the center it is
#this is not a normal compass, but a 3d compass that shows the direction of the target in 3d space, an elite dangerous compass

import cv2
import numpy as np
import pyautogui
import time
import os
import pytesseract
from PIL import Image
from PIL import ImageDraw
from PIL import ImageChops


#takes a screenshot and saves it to elite_dangerous_bot
def screen_shot():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'pictures/screen_shot.png')
    return myScreenshot

#converts the screenshot to mono color
def mono_color():
    image = Image.open('pictures/screen_shot.png')
    image = image.convert('L')
    image.save(r'pictures/gray_scale.png')
    image = image.point(lambda x: 0 if x < 100 else 255, '1')
    image.save(r'pictures/mono_color.png')
    return image

#finds where the compass is on screen, and returns the coordinates of the compass
def find_compass():
    compass = Image.open('pictures/compass_sample.png')
    compass_location = pyautogui.locateCenterOnScreen(compass, grayscale=True, confidence=0.7)
    if compass_location is not None:
        print(compass_location)
        bounds = 35
        box = (compass_location[0]-bounds, compass_location[1]-bounds, compass_location[0]+bounds, compass_location[1]+bounds)
        screen_shot().crop(box).save(r'pictures/found_compass.png')
    else:
        print('compass not found')

#finds the target on the compass, and returns the deviation from center
def target_deviation():
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
    deviation = (coords[0]-35, coords[1]-35)
    return deviation
    

def output(deviation):
    if abs(deviation[0]) < 4 and abs(deviation[1]) > 4:
        #target is horizontally centered
        if deviation[1] > 4:
            #target is above
            print('target is below')
        elif deviation[1] < -4:
            #target is below
            print('target is above')
    elif abs(deviation[0]) > 4:
        #target is not horizontally centered
        if deviation[0] > 4:
            #target is to the right
            print('target is to the right')
        elif deviation[0] < -4:
            #target is to the left
            print('target is to the left')
    elif abs(deviation[0]) < 4 and abs(deviation[1]) < 4:
        #target is centered
        print('target is centered')
    print(deviation)





while True:
    time.sleep(1)
    #screen_shot()
    #mono_color()
    find_compass()
    dev = target_deviation()
    output(dev)