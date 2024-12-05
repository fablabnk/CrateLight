# Initialize the Game of Life board

# Main loop for experimenting
while True:
    position = random.choice(['1', '0'])
    direction = random.choice(['1', '0'])
    light_up_grid(direction, position, 0.1, get_random_color())
    position = random.choice(['1', '0'])
    direction = random.choice(['1', '0'])
    light_up_grid(direction, position, 0.1, get_random_color())
    position = random.choice(['1', '0'])
    direction = random.choice(['1', '0'])
    light_up_grid(direction, position, 0.1, get_random_color())
    ft_draw(random.choice([True, False]))
    color = get_random_color()
    color2 = get_random_color()
    if color == color2:
        color = get_random_color()
    brd: list[list[int]] = [[0 if random.randint(0,100) <= 42 else 1 for _ in range(24)] for _ in range(12)]
    col = 0
    for i in range(42):
        draw_from_grid(brd, color, color2)
        brd = gol_step(brd)
        for _ in range(42):
            brd[random.randint(0, 11)][random.randint(0, 23)] = 1