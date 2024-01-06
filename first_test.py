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


#takes a screenshot and saves it to elite_dangerous_bot
def screen_shot():
    #takes a screenshot
    myScreenshot = pyautogui.screenshot()
    #saves the screenshot
    myScreenshot.save(r'elite_dangerous_bot/screen_shot.png')
    return myScreenshot

#converts the screenshot to mono color, with infinite contrast
def mono_color():
    image = Image.open('elite_dangerous_bot/screen_shot.png')
    #converts the screenshot to grayscale
    image = image.convert('L')
    #saves grayscale screenshot
    image.save(r'elite_dangerous_bot/gray_scale.png')
    #converts the screenshot to black and white
    image = image.point(lambda x: 0 if x < 100 else 255, '1')
    #saves the screenshot
    image.save(r'elite_dangerous_bot/mono_color.png')
    return image

#finds where the compass is on screen, and returns the coordinates of the compass
def find_compass():
    compass = Image.open('elite_dangerous_bot/compass_sample.png')
    compass_location = pyautogui.locateCenterOnScreen(compass, grayscale=True, confidence=0.7)
    if compass_location != None:
        print(compass_location)
        #draws a box around the found compass
        bounds = 45
        box = (compass_location[0]-bounds, compass_location[1]-bounds, compass_location[0]+bounds, compass_location[1]+bounds)
        #saves the screenshot
        screen_shot().crop(box).save(r'elite_dangerous_bot/found_compass.png')


    else:
        print('compass not found')

while True:
    time.sleep(1)
    #screen_shot()
    #mono_color()
    find_compass()