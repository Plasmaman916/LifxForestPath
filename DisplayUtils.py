from NoiseArray import NoiseArray
import pygame

def display(surface, noise_array: NoiseArray, width, height, x, y):
    l = len(noise_array)
    array = noise_array.clamp().arr
    for i in range(l):
        pygame.draw.rect(surface, array[i], pygame.Rect(i * width/l + x, y, width/l, height))

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_value = max(r, g, b)
    min_value = min(r, g, b)
    df = max_value - min_value

    if max_value == min_value:
        h = 0
    elif max_value == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif max_value == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif max_value == b:
        h = (60 * ((r - g) / df) + 240) % 360

    if max_value == 0:
        s = 0
    else:
        s = df / max_value

    v = max_value

    return (h,s,v)