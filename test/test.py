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

staring_time = 0  # how long I have been staring at the object
not_staring_time = 0  # if user is not staring it should be >0

gaze_prev = [0, 0]  # previous gaze data


# Define the gaze data callback function
def gaze_data_callback(gaze_data):
    global staring_time
    global not_staring_time
    global gaze_prev

    # Get the gaze point coordinates in pixels
    gaze_point = gaze_data['left_gaze_point_on_display_area']
    gaze_x = int(gaze_point[0] * pyautogui.size().width) - 2
    gaze_y = int(gaze_point[1] * pyautogui.size().height) - 4
    # Move the mouse cursor to the gaze point coordinates
    pyautogui.moveTo(gaze_x, gaze_y, 1)

    # if gazing at the object's width add 1 to the staring time
    # if object_pos[0] <= gaze_point[0] <= object_pos[0] + object_size[0]:
    #   staring_time += 1

    if abs(gaze_prev[0] - gaze_x) <= 80 or abs(gaze_prev[1] - gaze_y) <= 80:
        staring_time += 1
        not_staring_time = 0
    else:
        not_staring_time += 1
        staring_time = 0

    gaze_prev = gaze_x, gaze_y

    if not_staring_time >= 3:
        staring_time = 0

    # if staring_time is more than 5 seconds then click the component
    if staring_time == 4:
        pyautogui.click()
        not_staring_time = 0
        staring_time = 0

    print(staring_time)


while True:
    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    time.sleep(1)
    eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
