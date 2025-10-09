"""LED animation effects"""

import time
from .grid_utils import coords_to_id, ids_by_coord

def light_up_grid_horizontal(pixels, start, delay, color):
    """Light up grid horizontally from top or bottom"""
    if start.lower() in ['top', 't', '1']:
        for y in range(len(ids_by_coord)):
            for x in range(len(ids_by_coord[y])):
                index = coords_to_id(x, y)
                pixels[index] = color
            pixels.show()
            time.sleep(delay)
    elif start.lower() in ['bottom', 'b', '0']:
        for y in range(len(ids_by_coord) - 1, -1, -1):
            for x in range(len(ids_by_coord[y])):
                index = coords_to_id(x, y)
                pixels[index] = color
            pixels.show()
            time.sleep(delay)

def light_up_grid_vertical(pixels, start, delay, color):
    """Light up grid vertically from left or right"""
    if start.lower() in ['left', 'l', '1']:
        for x in range(len(ids_by_coord[0]) - 1, -1, -1):
            for y in range(len(ids_by_coord)):
                index = coords_to_id(x, y)
                pixels[index] = color
            pixels.show()
            time.sleep(delay)
    elif start.lower() in ['right', 'r', '0']:
        for x in range(len(ids_by_coord[0])):
            for y in range(len(ids_by_coord)):
                index = coords_to_id(x, len(ids_by_coord) - 1 - y)
                pixels[index] = color
            pixels.show()
            time.sleep(delay)

def light_up_grid(pixels, direction, start, delay, color):
    """Light up grid in specified direction and starting point"""
    if direction.lower() in ['horizontal', 'h', '1']:
        light_up_grid_horizontal(pixels, start, delay, color)
    if direction.lower() in ['vertical', 'v', '0']:
        light_up_grid_vertical(pixels, start, delay, color)
