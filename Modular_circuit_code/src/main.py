# Initialize the Game of Life board

brd: list[list[int]] = [[0 for _ in range(24)] for _ in range(12)]

brd[0][2] = 1
brd[1][0] = 1
brd[1][2] = 1
brd[2][1] = 1
brd[2][2] = 1

brd[5][2] = 1
brd[6][0] = 1
brd[6][2] = 1
brd[7][1] = 1
brd[7][2] = 1

brd[5][2+5] = 1
brd[6][0+5] = 1
brd[6][2+5] = 1
brd[7][1+5] = 1
brd[7][2+5] = 1

brd[0][2+5] = 1
brd[1][0+5] = 1
brd[1][2+5] = 1
brd[2][1+5] = 1
brd[2][2+5] = 1

brd[5][2+10] = 1
brd[6][0+10] = 1
brd[6][2+10] = 1
brd[7][1+10] = 1
brd[7][2+10] = 1

brd[0][2+10] = 1
brd[1][0+10] = 1
brd[1][2+10] = 1
brd[2][1+10] = 1
brd[2][2+10] = 1

brd[5][2+15] = 1
brd[6][0+15] = 1
brd[6][2+15] = 1
brd[7][1+15] = 1
brd[7][2+15] = 1

brd[0][2+15] = 1
brd[1][0+15] = 1
brd[1][2+15] = 1
brd[2][1+15] = 1
brd[2][2+15] = 1

# brd = FT

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
    for i in range(19):
        draw_from_grid(brd, color, color2)
        brd = gol_step(brd)