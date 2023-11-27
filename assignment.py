from __future__ import print_function

import time
from sr.robot import *

# Thresholds for control
a_th = 2.0
d_th = 0.4
"""a_th: Threshold for robot direction control."""
"""d_th: Threshold for linear distance control of the robot"""

# Robot instance
R = Robot()
"""R: An instance of the Robot class corresponding to the robot"""

# Function to adjust linear speed
""" The `drive` function adjusts the robot's linear speed for a specified duration, taking speed and time as input parameters."""
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

# Function to adjust angular speed
""" The `turn` function adjusts the robot's angular speed for a specified duration, taking speed and time as input parameters."""
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
""" `find_token_gold()` function searches for golden tokens using the robot's camera and sensors, returning distance and rotation data if a token is found."""    

def find_token_gold():
    distance = 100    
    for a in R.see():
        if a.dist < distance and a.info.marker_type == MARKER_TOKEN_GOLD:
            distance = a.dist
            rotation = a.rot_y
    if distance == 100:
        return -1, -1
    else:
        return distance, rotation 
# Returns distance and rotation data if a token is found.
"""distance: The distance from the robot to the token"""
"""rotation: The rotation of the robot relative to the token"""        


"""Index and Index2: Indices used in the while loops to determine the conditions for continuing the program execution"""
# Main loop
index = 1
while index:       
    distance, rotation = find_token_gold()
    while distance == -1:
        print("No tokens found!!")
        turn(5, 0.5)
        distance, rotation = find_token_gold()

    if distance < d_th:
        print("Found it!")
        R.grab()
        print("""Got it!""")
        index = 0
    elif -a_th <= rotation <= a_th:
        print("""we've arrived at our destination!""")
        drive(10, 0.8)
    elif rotation < -a_th:
        print("""Adjusting slightly to the left...""")
        turn(-2, 0.5)
    elif rotation > a_th:
        print("""Adjusting slightly to the right...""")
        turn(+2, 0.5)
# Post-token pickup actions
turn(-8, 1.5)
drive(30, 6)
R.release()
# Additional search loop
drive(-20, 1.5)
turn(-10, 4)
drive(20, 2)  

# Secondary loop for token collection
index2 = 0
while index2 < 5:
    distance, rotation = find_token_gold()
    while distance == -1:
        print("""I have not spotted any additional tokens. Continuing the search""")
        turn(+5, 0.5)
        distance, rotation = find_token_gold()
        
    if distance < d_th:
        print("Found it!")
        R.grab()
        print("""Got it!""")
        turn(20, 2.5)
        drive(22, 6)
        R.release()
        drive(-20, 1.5)
        turn(-10, 4)
        drive(20, 2)
        index2 += 1
    elif -a_th <= rotation <= a_th:
        print("""we've arrived at our destination!""")
        drive(10, 0.8)
    elif rotation < -a_th:
        print("""Adjusting slightly to the left...""")
        turn(-2, 0.5)
    elif rotation > a_th:
        print("""Adjusting slightly to the right...""")
        turn(+2, 0.5)

