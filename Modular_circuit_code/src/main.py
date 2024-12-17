import random
from chase_fill import light_up_grid
from colors import get_random_color
from grid_utils import draw_from_grid
from game_of_life import gol_step, brd
from fortytwo import ft_draw

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