from perlin_noise import PerlinNoise
from NoiseArray import NoiseArray
from math import floor

def clamp(val, minimum, maximum):
    return max(min(val, maximum), minimum)

class LinearNoise:
    def __init__(self, time, r, h, octaves, seed, t_time, c_time, color_mask: tuple, background: tuple):
        self.last_time = time
        self.current_time = time
        self.transition_start = time
        self.r = r
        self.h = h
        self.octaves = octaves
        self.init_seed = seed
        self.seed = seed
        self.t_time = t_time
        self.c_time = c_time
        self.current_vals = [0] * r
        self.next_vals = [0] * r
        self.disp_vals = [0] * r
        self.transition_done = True
        self.color_mask = color_mask
        self.background = background

        self.next_noise = PerlinNoise(octaves=self.octaves, seed=self.seed)
        self.current_noise = PerlinNoise(octaves=self.octaves, seed=self.seed)

    def set_seed_offset(self, seed):
        self.seed = self.init_seed + seed

    def get_raw_vals(self):
        return self.disp_vals

    def get_color_vals(self):
        ret_vals = [0] * self.r
        for i in range(self.r):
            color_val = self.disp_vals[i]
            color = (
                clamp(color_val * self.color_mask[0] + self.background[0], 0, 255),
                clamp(color_val * self.color_mask[1] + self.background[1], 0, 255),
                clamp(color_val * self.color_mask[2] + self.background[2], 0, 255)
            )
            ret_vals[i] = color
        ret_arr = NoiseArray(self.r, array=ret_vals)
        return ret_arr

    def r(self):
        return self.r

    def display_vals(self, pygame, surface, width, height, x, y):
        rect_width = (width / self.r)
        rect_height = height / 3
        for i in range(self.r):
            color_val = self.disp_vals[i]
            color = (
                clamp(color_val * self.color_mask[0] + self.background[0], 0, 255),
                clamp(color_val * self.color_mask[1] + self.background[1], 0, 255),
                clamp(color_val * self.color_mask[2] + self.background[2], 0, 255)
                     )
            pygame.draw.rect(surface, color, pygame.Rect(i * rect_width + x, rect_height * 2 + y, rect_width, rect_height))

            color_val = self.current_vals[i]
            color = (
                clamp(color_val * self.color_mask[0]  + self.background[0], 0, 255),
                clamp(color_val * self.color_mask[1] + self.background[1], 0, 255),
                clamp(color_val * self.color_mask[2] + self.background[2], 0, 255)
            )
            pygame.draw.rect(surface, color, pygame.Rect(i * rect_width + x, rect_height + y, rect_width, rect_height))

            color_val = self.next_vals[i]
            color = (
                clamp(color_val * self.color_mask[0] + self.background[0], 0, 255),
                clamp(color_val * self.color_mask[1] + self.background[1], 0, 255),
                clamp(color_val * self.color_mask[2] + self.background[2], 0, 255)
            )
            pygame.draw.rect(surface, color, pygame.Rect(i * rect_width + x, y, rect_width, rect_height))

    def step(self, time):
        self.current_time = time
        if self.current_time >= self.transition_start + self.t_time:
            self.current_noise = self.next_noise
            self.seed = self.seed + 37.14159265358979323846124338

            self.next_noise = PerlinNoise(octaves=self.octaves, seed=self.seed)
            for i in range(self.r):
                next_n = abs(self.next_noise(i / self.r) * self.h)
                current_n = abs(self.current_noise(i / self.r) * self.h)
                self.current_vals[i] = current_n
                self.next_vals[i] = next_n
            self.transition_start = time

        self.disp_vals = [0] * self.r
        for i in range(self.r):
            diff_val = self.next_vals[i] - self.current_vals[i]
            self.disp_vals[i] = self.current_vals[i] + (diff_val * (self.current_time - self.transition_start) / self.t_time)