from NoiseArray import NoiseArray
import pygame

def display(surface, noise_array: NoiseArray, width, height, x, y):
    l = len(noise_array)
    array = noise_array.clamp().arr
    for i in range(l):
        pygame.draw.rect(surface, array[i], pygame.Rect(i * width/l + x, y, width/l, height))
