# Initialize the Game of Life board

# Main loop for experimenting
while True:
    color = get_random_color()
    color2 = get_random_color()
    brd: list[list[int]] = [[0 if 75 < 50 else 1 for _ in range(24)] for _ in range(12)]
    col = 0
    for i in range(100):
        draw_from_grid(brd, color, color2)
        #for ro in brd:
        #    print("".join(["#" if x == 1 else " " for x in ro]))
        brd = gol_step(brd)
        brd[col] = [1 for _ in range(24)]
        col += 2
        if col == 12:
            col = 0
    # Draw the current state of the Game of Life
 

    # Light up the grid with random colors
    position = random.choice(['1', '0'])
    direction = random.choice(['1', '0'])
    light_up_grid(direction, position, 0.1, get_random_color())
    position = random.choice(['1', '0'])
    direction = random.choice(['1', '0'])
    light_up_grid(direction, position, 0.1, get_random_color())
    position = random.choice(['1', '0'])
    direction = random.choice(['1', '0'])
    light_up_grid(direction, position, 0.1, get_random_color())

    time.sleep(0.5)  # Delay for visualization