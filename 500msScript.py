###################################################################
# Notes:                                                          #
# 1) Find object's position and size                              #
# 2) Cursor moving works kinda - not too accurate                 #
###################################################################

import tobii_research as tr
import pyautogui
import time

found_eyetrackers = tr.find_all_eyetrackers()
eyetracker = found_eyetrackers[0]
gaze_prev = [0, 0]  # previous gaze data
logstart = time.time()


# Define the gaze data callback function
def gaze_data_callback(gaze_data):
    global gaze_prev
    global logstart

    # Get the gaze point coordinates in pixels
    gaze_point = gaze_data['left_gaze_point_on_display_area']
    gaze_x = int(gaze_point[0] * pyautogui.size().width)
    gaze_y = int(gaze_point[1] * pyautogui.size().height)
    # Move the mouse cursor to the gaze point coordinates
    pyautogui.moveTo(gaze_x, gaze_y, 0.5)

    # if gazing at the object's width add 1 to the staring time
    if (abs(gaze_prev[0] - gaze_x) <= 80 or abs(gaze_prev[1] - gaze_y) <= 80) and (time.time()-0.500 >= logstart):
        pyautogui.click()
        logstart = time.time()
    gaze_prev = gaze_x, gaze_y


while True:
    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    time.sleep(0.1)
    eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
