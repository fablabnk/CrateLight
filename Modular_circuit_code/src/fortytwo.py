import random
from colors import get_random_color 
from grid_utils import draw_from_grid 


FT: list[list[int]] = [
    [0,0,0,0,0,0,0,0,0,0,0,0,       0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,0,0,       0,0,0,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,0,0,       0,0,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,1,1,1,1,0,0,       0,1,1,1,0,0,0,0,1,1,0,0],
    [0,0,0,0,0,1,1,0,1,1,0,0,       0,0,0,0,0,0,0,1,1,1,0,0],
    [0,0,0,0,1,1,0,0,1,1,0,0,       0,0,0,0,0,0,1,1,1,0,0,0],
    [0,0,0,1,1,0,0,0,1,1,0,0,       0,0,0,0,1,1,1,1,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,0,       0,0,1,1,1,1,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,0,       0,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,0,0,       0,1,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,0,0,       0,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,1,1,0,0,       0,1,1,1,1,1,1,1,1,1,0,0]
]

def shift_columns(matrix: list[list[int]], shift_by: int, left: bool = False) -> list[list[int]]:
    """
    Shift the columns of a 2D array cyclically to the right or left.
    Args:
    - matrix: 2D list of integers.
    - shift_by: Number of positions to shift.
        Positive for right shift, negative for left shift.
    Returns:
    - The modified matrix with columns shifted.
    """
    num_cols = len(matrix[0])
    shift_by %= num_cols
    shifted_matrix = []
    for row in matrix:
        shifted_row = row[-shift_by:] + row[:-shift_by] if not left else row[shift_by:] + row[:shift_by]
        shifted_matrix.append(shifted_row)
    return shifted_matrix

def shift_rows(matrix: list[list[int]], shift_by: int, down: bool = True) -> list[list[int]]:
    """
    Shift the rows of a 2D array cyclically up or down.
    Args:
    - matrix: 2D list of integers.
    - shift_by: Number of positions to shift.
        Positive for down shift, negative for up shift.
    Returns:
    - The modified matrix with rows shifted.
    """
    num_rows = len(matrix)
    shift_by %= num_rows
    shifted_matrix = matrix[-shift_by:] + matrix[:-shift_by] if down else matrix[shift_by:] + matrix[:shift_by]
    return shifted_matrix

def ft_draw(vertical: bool = False) -> None:
    i: int = 0
    grd = FT
    if not vertical:
        left = random.choice([True, False])
        while True:
            color = (0,0,0) #COLORS["WHITE"] #get_random_color()
            color2 = get_random_color()
            if color == color2:
                color = get_random_color()
            if i >= 10 and i <= 34:
                grd = shift_columns(FT, (i-10)%24, left)
            draw_from_grid(grd, color, color2)
            i += 1
            if i == 44:
                return
    else:
        down = random.choice([True, False])
        while True:
            color = (0,0,0)
            color2 = get_random_color()
            if color == color2:
                color = get_random_color()
            if i >= 10 and i <= 22:
                grd = shift_rows(FT, (i-10)%12, down)
            draw_from_grid(grd, color, color2)
            i += 1
            if i == 32:
                return

