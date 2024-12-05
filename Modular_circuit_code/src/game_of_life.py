# game_of_life.py
# Game of Life step function
def gol_step(brd: list[list[int]]) -> list[list[int]]:
    """Performs one step in the Game of Life."""
    next_brd = [row[:] for row in brd]  # Create a copy of the board for updates
    for y in range(len(brd)):
        for x in range(len(brd[y])):
            neighbors = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    if 0 <= y + dy < len(brd) and 0 <= x + dx < len(brd[y]):
                        neighbors += brd[y + dy][x + dx]
            if brd[y][x] == 1:  # Cell is alive
                if neighbors < 2 or neighbors > 3:
                    next_brd[y][x] = 0
            else:  # Cell is dead
                if neighbors == 3:
                    next_brd[y][x] = 1
    return next_brd

