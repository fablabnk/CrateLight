
# turn off all 
def clear_grid():
    for i in range(num_leds):
        pixels[i] = OFF
    pixels.show()

# color border
def borders(rows, cols):
    for i in range(num_leds):
        if ((i + 1) % 25 == 0):
            continue
        elif coords_by_id[i][0] == 0 or coords_by_id[i][0] == 23:
            pixels[i] = Colors["GREEN"]
        elif coords_by_id[i][1] == 0 or coords_by_id[i][1] == 11:
            pixels[i] = Colors["GREEN"]
        else:
            pixels[i] = Colors["WHITE"]
    pixels.show()
    time.sleep(0.5)

# color by coordinates
def color_coords(x, y):
    index = coords_to_id(x, y)
    if index is not None:
        pixels[index - 1] = Colors["RED"]
        pixels.show()
    time.sleep(0.5)

# color by led id
def color_id(id):
    pixels[id] = Colors["GREEN"]
    pixels.show()

def draw_from_grid(drawing, color1, color2):
    for y in range(12):
        for x in range(24):
            index = coords_to_id(x, y)
            if drawing[y][x] == 1:
                pixels[index ] = color1
            else:
                pixels[index] = color2
    pixels.show()
    time.sleep(0.5)

# not working well
def move_right():
    for y in range(12):
        for x in range(24):
            index_left = coords_to_id(x, y)
            index = coords_to_id(x, y)
            if pixels[index_left] == Colors["GREEN"]:
                pixels[index] = Colors["GREEN"]
                pixels[index_left] = Colors["OFF"]
        pixels.show()
    time.sleep(0.5)

# Main loop for experimenting
while True:
    delay_in_seconds = 60 / (4000)
    position = random.choice(['1', '0'])
    direction = random.choice(['1', '0'])
    light_up_grid(direction, position, delay_in_seconds, get_random_color())
    position = random.choice(['1', '0'])
    direction = random.choice(['1', '0'])
    light_up_grid(direction, position, delay_in_seconds, get_random_color())
