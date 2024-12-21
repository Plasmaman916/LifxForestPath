import random
import time
import pygame
from lifxlan import Light, MultiZoneLight, LifxLAN
import colorsys

from LinearNoise import LinearNoise
from NoiseArray import NoiseArray
import DisplayUtils

lights = [MultiZoneLight('d0:73:d5:d4:bd:a4', '192.168.1.177'),MultiZoneLight('d0:73:d5:43:9b:d6', '192.168.1.212')]
lights[0].set_power(True, 0, True)
lights[1].set_power(True, 0, True)

# lan = LifxLAN()
# lights = lan.get_lights()
# time.sleep(1)
# for n in lights:
#     print(n)

pygame.init()

width = 1000
height = 800

# surface = pygame.display.set_mode((width,height))

keepGameRunning = True
last_time = time.time()

r = 30

blue_color = (110/2, 141/2, 200/2)

blue = LinearNoise(last_time,r,7, 6, 0, 1, 1,(-100, -100, -100), blue_color)
blue_inv = LinearNoise(last_time,r,3, 5, 872, 2, 1,blue_color, (0, 0, 0))
blue_inv2 = LinearNoise(last_time,r,3, 3, 123, 3, 1,blue_color, (0, 0, 0))
green_a = LinearNoise(last_time,r,3, 5, 872, 2, 1,(20, 181, 60), (0, 0, 50))
green_a2 = LinearNoise(last_time,r,3, 3, 123, 3, 1,(20, 181, 60), (0, 0, 0))

bluea = LinearNoise(last_time,r,7, 6, 1000, 1, 1,(-100, -100, -100), blue_color)
blue_inva = LinearNoise(last_time,r,3, 5, 88888, 2, 1,blue_color, (0, 0, 0))
blue_inv2a = LinearNoise(last_time,r,3, 3, 3327, 3, 1,blue_color, (0, 0, 0))
green_aa = LinearNoise(last_time,r,3, 5, 88888, 2, 1,(20, 181, 60), (0, 0, 50))
green_a2a = LinearNoise(last_time,r,3, 3, 3327, 3, 1,(20, 181, 60), (0, 0, 0))

lights[0].set_zone_color(1, 49, [0,0,65535, 3000], 0, True, apply=1)
lights[1].set_zone_color(1, 49, [0,0,65535, 3000], 0, True, apply=1)

def rand_time():
    return random.random()*10 + 15

last_ran = time.time()
new_run = last_ran + rand_time()
new_run_end = new_run + 5
new_run1 = new_run + 2
new_run_end1 = new_run_end + 2
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           keepGameRunning = False

    current_time = time.time()

    blue.step(current_time)
    blue_inv.step(current_time)
    blue_inv2.step(current_time)
    green_a.step(current_time)
    green_a2.step(current_time)

    bluea.step(current_time)
    blue_inva.step(current_time)
    blue_inv2a.step(current_time)
    green_aa.step(current_time)
    green_a2a.step(current_time)

    blue_vals = blue.get_color_vals()
    blue_inv_vals = blue_inv.get_color_vals()
    blue_inv2_vals = blue_inv2.get_color_vals()
    green_a_vals = green_a.get_color_vals()
    green_a2_vals = green_a2.get_color_vals()

    blue_valsa = bluea.get_color_vals()
    blue_inv_valsa = blue_inva.get_color_vals()
    blue_inv2_valsa = blue_inv2a.get_color_vals()
    green_a_valsa = green_aa.get_color_vals()
    green_a2_valsa = green_a2a.get_color_vals()

    # DisplayUtils.display(surface, blue_vals, width, 100, 0, 0)
    # # DisplayUtils.display(surface, blue_inv_vals, width, 100, 0, 100)
    # # DisplayUtils.display(surface, green_a_vals, width, 100, 0, 200)
    # # DisplayUtils.display(surface, blue_inv2_vals, width, 100, 0, 300)
    # # DisplayUtils.display(surface, green_a2_vals, width, 100, 0, 400)
    # DisplayUtils.display(surface, blue_vals.sub(blue_inv_vals).add(green_a_vals), width, 100, 0, 500)
    # DisplayUtils.display(surface, blue_vals.sub(blue_inv2_vals).add(green_a2_vals), width, 100, 0, 600)

    final_vals: NoiseArray = blue_vals.sub(blue_inv2_vals*0.7).sub(blue_inv_vals*0.7).add(green_a2_vals*0.7).add(green_a_vals*0.7).clamp()
    final_valsa: NoiseArray = blue_valsa.sub(blue_inv2_valsa*0.7).sub(blue_inv_valsa*0.7).add(green_a2_valsa*0.7).add(green_a_valsa*0.7).clamp()

    # DisplayUtils.display(surface, blue_vals.sub(blue_inv2_vals*0.7).sub(blue_inv_vals*0.7).add(green_a2_vals*0.7).add(green_a_vals*0.7), width, 100, 0, 700)

    if current_time > new_run_end1:
        new_time()

    numbers = list(range(len(final_vals.arr)))
    random.shuffle(numbers)
    out = ""
    for i in numbers:
        color = colorsys.rgb_to_hsv(final_vals.arr[i][0]/255.0, final_vals.arr[i][1]/255.0, final_vals.arr[i][2]/255.0)
        colora = colorsys.rgb_to_hsv(final_valsa.arr[i][0]/255.0, final_valsa.arr[i][1]/255.0, final_valsa.arr[i][2]/255.0)
        out += str(color) + " "
        # print(out)
        side0_del = 400
        side1_del = 400
        if new_run < current_time < new_run_end:
            if start_side == 0:
                side0_del = 0
            else:
                side1_del = 0
        if new_run1 < current_time < new_run_end1:
            if start_side == 1:
                side0_del = 0
            else:
                side1_del = 0
        lights[0].set_zone_color(0 + i, 0 + i, [color[0]*60000, color[1]*60000, color[2]*60000, 3000], side0_del, True, apply=1)
        lights[1].set_zone_color(0 + i, 0 + i, [colora[0]*60000, colora[1]*60000, colora[2]*60000, 3000], side1_del, True, apply=1)
        time.sleep(0.02)


    # pygame.display.flip()

    last_time = time.time()
