"""Utility functions for LED effects"""

import math


def wheel(pos):
    """
    Generate rainbow RGB colors from 0-255 position on color wheel

    Args:
        pos: Position on color wheel (0-255)

    Returns:
        tuple: (R, G, B) color values
    """
    pos = int(pos) % 256
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)


def scale_color(color, brightness):
    """
    Scale a color by brightness factor

    Args:
        color: (R, G, B) tuple
        brightness: 0.0 to 1.0

    Returns:
        tuple: Scaled (R, G, B) color
    """
    return (
        int(color[0] * brightness),
        int(color[1] * brightness),
        int(color[2] * brightness)
    )


def sine_wave(phase, power=1.0):
    """
    Generate smooth sine wave value from phase

    Args:
        phase: 0.0 to 1.0
        power: Exponent to apply (default 1.0). Use 2.0 for smoother pulse

    Returns:
        float: 0.0 to 1.0
    """
    return (math.sin(phase * math.pi)) ** power


def lerp_color(color1, color2, t):
    """
    Linear interpolation between two colors

    Args:
        color1: (R, G, B) start color
        color2: (R, G, B) end color
        t: 0.0 to 1.0 interpolation factor

    Returns:
        tuple: Interpolated (R, G, B) color
    """
    return (
        int(color1[0] + (color2[0] - color1[0]) * t),
        int(color1[1] + (color2[1] - color1[1]) * t),
        int(color1[2] + (color2[2] - color1[2]) * t)
    )


def gol_step(board):
    """
    Compute one step of Conway's Game of Life with wrapping edges

    Rules:
    - Any live cell with 2 or 3 neighbors survives
    - Any dead cell with exactly 3 neighbors becomes alive
    - All other cells die or stay dead

    Args:
        board: 2D list representing the game board (0=dead, 1=alive)

    Returns:
        list: New 2D board after one step
    """
    height = len(board)
    width = len(board[0]) if height > 0 else 0
    new_board = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            # Count live neighbors (with wrapping)
            neighbors = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    # Wrap around edges (toroidal topology)
                    ny = (y + dy) % height
                    nx = (x + dx) % width
                    neighbors += board[ny][nx]

            # Apply Game of Life rules
            if board[y][x] == 1:  # Cell is alive
                new_board[y][x] = 1 if neighbors in [2, 3] else 0
            else:  # Cell is dead
                new_board[y][x] = 1 if neighbors == 3 else 0

    return new_board
