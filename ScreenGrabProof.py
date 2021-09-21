# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 18:08:59 2021

@author: Chris
"""

#%% Imports

from PIL import ImageGrab
import win32gui
import numpy as np
import time
import cv2

#%% Get the ID of the Emulator window

# List to hold window information
window = []
# Name of the window to find
window_name = "Super Street Fighter II (USA) - Snes9x 1.60"

# Function to extract emulator window information
# Given a window and checks if its visible and if it matches the required name
# IF the above are true then we add the information to the window list
def winEnumHandler(hwnd, ctx, window_name=window_name):
    if win32gui.IsWindowVisible(hwnd):
        print(win32gui.GetWindowText(hwnd))
        if win32gui.GetWindowText(hwnd) == window_name:
            window.append(hwnd)
            window.append(win32gui.GetWindowText(hwnd))

# Function to get the screen
# Uses the enumerate windows function from wn32gui with our handler to get the
# correct window.
win32gui.EnumWindows(winEnumHandler, None)

#%% Window streaming

# Pixelwise relative corrections for the window bounding box
screen_correction = np.array([-8,-51,8,8])

# Loop to capture the window
while True:
    try:
        # Get the start time
        start_time = time.time()
        
        # Get the bounding box for the window
        bbox = np.array(win32gui.GetWindowRect(window[0]))
        # Correct the window size
        bbox = tuple(bbox - screen_correction)
        # Get the screen capture
        screen_grab = np.array(ImageGrab.grab(bbox))
        
        # Prints the time it took to collect the screenshot
        print(f"loop took {time.time()-start_time} seconds")
        
        # Reset the start time for the next loop
        start_time=time.time()
        
        # Display the image in a new window
        cv2.imshow("window", cv2.cvtColor(screen_grab, cv2.COLOR_BGR2RGB))
        # Checks to see if window should be closed and loop stopped
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
    except Exception as e:
        print("error", e)
# %%
