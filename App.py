import colorsys
import random
import time

from lifxlan import MultiZoneLight
import pygame

import DisplayUtils
from LinearNoise import LinearNoise
from NoiseArray import NoiseArray

SIMULATION = False

lights = [MultiZoneLight('d0:73:d5:d4:bd:a4', '192.168.1.177'),
          MultiZoneLight('d0:73:d5:43:9b:d6', '192.168.1.212')]

pygame.init()

# Used for displaying simulation
width = 900
height = 800

if SIMULATION:
    surface = pygame.display.set_mode((width,height))

keepGameRunning = True
curr_time = time.time()

# number of segments or 'columns'
cols = 30

# Background 'sky' color
blue_color = (110/2, 141/2, 200/2)

# Define all of the color masks
blue_l = LinearNoise(curr_time, cols,7, 6, 0, 1, 1,(-100, -100, -100), blue_color)
blue_inv_l = LinearNoise(curr_time, cols,3, 5, 872, 2, 1,blue_color, (0, 0, 0))
blue_inv2_l = LinearNoise(curr_time, cols,3, 3, 123, 3, 1,blue_color, (0, 0, 0))
green_l = LinearNoise(curr_time, cols,3, 5, 872, 2, 1,(20, 181, 60), (0, 0, 50))
green2_l = LinearNoise(curr_time, cols,3, 3, 123, 3, 1,(20, 181, 60), (0, 0, 0))

blue_r = LinearNoise(curr_time, cols,7, 6, 0, 1, 1,(-100, -100, -100), blue_color)
blue_inv_r = LinearNoise(curr_time, cols,3, 5, 872, 2, 1,blue_color, (0, 0, 0))
blue_inv2_r = LinearNoise(curr_time, cols,3, 3, 123, 3, 1,blue_color, (0, 0, 0))
green_r = LinearNoise(curr_time, cols,3, 5, 872, 2, 1,(20, 181, 60), (0, 0, 50))
green2_r = LinearNoise(curr_time, cols,3, 3, 123, 3, 1,(20, 181, 60), (0, 0, 0))

# Set the end of the strings to a constant white clor
lights[0].set_zone_color(1, 49, [0,0,65535, 3000], 0, True, apply=1)
lights[1].set_zone_color(1, 49, [0,0,65535, 3000], 0, True, apply=1)

def rand_time():
    return random.random()*10 + 15

# Define variables for wind effect
last_ran = time.time()
new_run = last_ran + rand_time() # Next wind effect start time for left side
new_run_end = new_run + 5 # Next wind effect end time for left side
new_run1 = new_run + 2 # Next wind effect start time for right side
new_run_end1 = new_run_end + 2 # Next wind effect end time for right side
start_side = 0

def new_time():
    global last_ran
    global new_run
    global new_run_end
    global start_side
    global new_run1
    global new_run_end1
    last_ran = time.time()
    new_run = last_ran + rand_time()
    new_run_end = new_run + 5
    new_run1 = new_run + 2
    new_run_end1 = new_run_end + 2
    start_side = random.randint(0,1)


while keepGameRunning:
    if SIMULATION:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               keepGameRunning = False

    current_time = time.time()

    # Step the color simulations
    blue_l.step(current_time)
    blue_inv_l.step(current_time)
    blue_inv2_l.step(current_time)
    green_l.step(current_time)
    green2_l.step(current_time)

    blue_r.step(current_time)
    blue_inv_r.step(current_time)
    blue_inv2_r.step(current_time)
    green_r.step(current_time)
    green2_r.step(current_time)


    # Get all the current colors
    blue_vals_l = blue_l.get_color_vals()
    blue_inv_vals_l = blue_inv_l.get_color_vals()
    blue_inv2_vals_l = blue_inv2_l.get_color_vals()
    green_vals_l = green_l.get_color_vals()
    green2_vals_l = green2_l.get_color_vals()

    blue_vals_r = blue_r.get_color_vals()
    blue_inv_vals_r = blue_inv_r.get_color_vals()
    blue_inv2_vals_r = blue_inv2_r.get_color_vals()
    green_vals_r = green_r.get_color_vals()
    green2_vals_r = green2_r.get_color_vals()


    # If we want to display the simulation, do it here
    # Only showing one side for simplicity
    if SIMULATION:
        DisplayUtils.display(surface, blue_vals_l, width, 100, 0, 0)
        DisplayUtils.display(surface, blue_inv_vals_l, width, 100, 0, 100)
        DisplayUtils.display(surface, green_vals_l, width, 100, 0, 200)
        DisplayUtils.display(surface, blue_inv2_vals_l, width, 100, 0, 300)
        DisplayUtils.display(surface, green2_vals_l, width, 100, 0, 400)
        DisplayUtils.display(surface,
                             blue_vals_l
                             .sub(blue_inv_vals_l)
                             .add(green_vals_l), width, 100, 0, 500)
        DisplayUtils.display(surface,
                             blue_vals_l
                             .sub(blue_inv2_vals_l)
                             .add(green2_vals_l), width, 100, 0, 600)
        DisplayUtils.display(surface,
                             blue_vals_l
                             .sub(blue_inv2_vals_l*0.7)
                             .sub(blue_inv_vals_l*0.7)
                             .add(green2_vals_l*0.7)
                             .add(green_vals_l*0.7), width, 100, 0, 700)


    # Add the masks together appropriately
    final_vals: NoiseArray = (blue_vals_l
                              .sub(blue_inv2_vals_l*0.7)
                              .sub(blue_inv_vals_l*0.7)
                              .add(green2_vals_l*0.7)
                              .add(green_vals_l*0.7)
                              .clamp())
    final_valsa: NoiseArray = (blue_vals_l
                               .sub(blue_inv2_vals_l*0.7)
                               .sub(blue_inv_vals_l*0.7)
                               .add(green2_vals_l*0.7)
                               .add(green_vals_l*0.7)
                               .clamp())

    # If wind effect is over, reset the timings
    if current_time > new_run_end1:
        new_time()

    # Update the segments in a random order to make it appear more natural
    numbers = list(range(len(final_vals.arr)))
    random.shuffle(numbers)
    for i in numbers:
        # Convert the RGB colors to HSV
        color_l = colorsys.rgb_to_hsv(final_vals.arr[i][0]/255.0, final_vals.arr[i][1]/255.0, final_vals.arr[i][2]/255.0)
        color_r = colorsys.rgb_to_hsv(final_valsa.arr[i][0]/255.0, final_valsa.arr[i][1]/255.0, final_valsa.arr[i][2]/255.0)

        # Default transition delays
        # This is how fast the segment changes to the new color
        side_l_del = 400
        side_r_del = 400
        # Apply faster transition for wind effect as needed
        if new_run < current_time < new_run_end:
            if start_side == 0:
                side_l_del = 0
            else:
                side_r_del = 0
        if new_run1 < current_time < new_run_end1:
            if start_side == 1:
                side_l_del = 0
            else:
                side_r_del = 0

        # Set the zone color for each segment
        # Need to multiply by 60000 to make it compatible with LIFX range
        lights[0].set_zone_color(0 + i, 0 + i, [color_l[0]*60000, color_l[1]*60000, color_l[2]*60000, 3000], side_l_del, True, apply=1)
        lights[1].set_zone_color(0 + i, 0 + i, [color_r[0]*60000, color_r[1]*60000, color_r[2]*60000, 3000], side_r_del, True, apply=1)
        # Sleep between packet send to each device due to packet rate limitations
        time.sleep(0.02)

    if SIMULATION:
        pygame.display.flip()