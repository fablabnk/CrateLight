"""Grid coordinate mapping and LED control utilities"""

import time

# Define your LED coordinate mapping
ids_by_coord = [
    [297, 298, 287, 286, 279, 278, 270, 269, 262, 261, 254, 253, 245, 244, 237, 236, 229, 228, 220, 219, 212, 211, 204, 203],
    [296, 295, 288, 285, 280, 277, 271, 268, 263, 260, 255, 252, 246, 243, 238, 235, 230, 227, 221, 218, 213, 210, 205, 202],
    [293, 294, 289, 284, 281, 276, 272, 267, 264, 259, 256, 251, 247, 242, 239, 234, 231, 226, 222, 217, 214, 209, 206, 201],
    [292, 291, 290, 283, 282, 275, 273, 266, 265, 258, 257, 250, 248, 241, 240, 233, 232, 225, 223, 216, 215, 208, 207, 200],
    [106, 107, 108, 115, 116, 123, 125, 132, 133, 140, 141, 148, 150, 157, 158, 165, 166, 173, 175, 182, 183, 190, 191, 198],
    [105, 104, 109, 114, 117, 122, 126, 131, 134, 139, 142, 147, 151, 156, 159, 164, 167, 172, 176, 181, 184, 189, 192, 197],
    [102, 103, 110, 113, 118, 121, 127, 130, 135, 138, 143, 146, 152, 155, 160, 163, 168, 171, 177, 180, 185, 188, 193, 196],
    [101, 100, 111, 112, 119, 120, 128, 129, 136, 137, 144, 145, 153, 154, 161, 162, 169, 170, 178, 179, 186, 187, 194, 195],
    [97, 98, 87, 86, 79, 78, 70, 69, 62, 61, 54, 53, 45, 44, 37, 36, 29, 28, 20, 19, 12, 11, 4, 3],
    [96, 95, 88, 85, 80, 77, 71, 68, 63, 60, 55, 52, 46, 43, 38, 35, 30, 27, 21, 18, 13, 10, 5, 2],
    [93, 94, 89, 84, 81, 76, 72, 67, 64, 59, 56, 51, 47, 42, 39, 34, 31, 26, 22, 17, 14, 9, 6, 1],
    [92, 91, 90, 83, 82, 75, 73, 66, 65, 58, 57, 50, 48, 41, 40, 33, 32, 25, 23, 16, 15, 8, 7, 0]
]

# Map coordinates to the LED ID
def coords_to_id(x, y):
    """Convert grid coordinates (x, y) to LED ID"""
    try:
        return ids_by_coord[y][x]
    except IndexError:
        return None

# Map LED ID to coordinates
def id_to_coords(led_id):
    """Convert LED ID to grid coordinates (x, y)"""
    for y, row in enumerate(ids_by_coord):
        for x, id in enumerate(row):
            if id == led_id:
                return (x, y)
    return None

def clear_grid(pixels, num_leds, off_color=(0, 0, 0)):
    """Turn off all LEDs"""
    for i in range(num_leds):
        pixels[i] = off_color
    pixels.show()

def borders(pixels, num_leds, coords_by_id, color1, color2):
    """Color border with color1 and interior with color2"""
    for i in range(num_leds):
        if ((i + 1) % 25 == 0):
            continue
        elif coords_by_id[i][0] == 0 or coords_by_id[i][0] == 23:
            pixels[i] = color1
        elif coords_by_id[i][1] == 0 or coords_by_id[i][1] == 11:
            pixels[i] = color1
        else:
            pixels[i] = color2
    pixels.show()
    time.sleep(0.5)

def color_coords(pixels, x, y, color):
    """Color a specific coordinate (x, y)"""
    index = coords_to_id(x, y)
    if index is not None:
        pixels[index - 1] = color
        pixels.show()
    time.sleep(0.5)

def color_id(pixels, id, color):
    """Color a specific LED by its ID"""
    pixels[id] = color
    pixels.show()

def draw_from_grid(pixels, drawing, color1, color2):
    """Draw a pattern from a 2D grid array"""
    for y in range(12):
        for x in range(24):
            index = coords_to_id(x, y)
            if drawing[y][x] == 1:
                pixels[index] = color1
            else:
                pixels[index] = color2
    pixels.show()
    time.sleep(0.5)
