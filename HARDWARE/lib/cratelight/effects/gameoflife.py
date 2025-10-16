"""Conway's Game of Life effect"""

import random
from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..utils import gol_step, wheel
from ..colors import COLORS, get_random_color


class GameOfLife(Effect, BPMSyncedEffect):
    """
    Conway's Game of Life on LED grid

    Usage:
        manager.add_effect(GameOfLife, beats=8, rainbow=True)  # Rainbow cycling colors
        manager.add_effect(GameOfLife, beats=8)  # Random colors (default)
    """

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None, rainbow=False):
        """
        Initialize Game of Life effect

        Args:
            rainbow: Cycle through rainbow colors on each reseed
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.rainbow = rainbow
        self.rainbow_offset = 0

    def setup(self):
        """Initialize the game board with random patterns"""
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.prev_board = None
        self.stuck_counter = 0
        self.dead_color = COLORS["OFF"]
        self.rainbow_offset = 0
        self._seed_random_pattern()

    def _seed_random_pattern(self):
        """Seed the board with random live cells"""
        # Clear board
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # Choose color based on mode
        if self.rainbow:
            # Rainbow cycling mode
            self.alive_color = wheel(self.rainbow_offset)
            self.rainbow_offset = (self.rainbow_offset + 40) % 256
        else:
            # Extended random color choices
            color_choices = [COLORS["RED"], COLORS["GREEN"], COLORS["BLUE"],
                            COLORS["YELLOW"], COLORS["CYAN"], COLORS["MAGENTA"],
                            COLORS["PURPLE"], COLORS["ORANGE"], COLORS["WHITE"],
                            (255, 50, 0),   # Red-orange
                            (0, 255, 128),  # Spring green
                            (128, 0, 255),  # Purple-blue
                            (255, 0, 128)]  # Hot pink
            self.alive_color = random.choice(color_choices)

        # Pick a random color for dead cells (70% chance of OFF, 30% chance of dim color)
        if random.randint(0, 9) < 7:
            self.dead_color = COLORS["OFF"]
        else:
            # Use a different color from alive, dimmed down
            if self.rainbow:
                # Use complementary color for dead cells
                dead_base = wheel((self.rainbow_offset + 128) % 256)
            else:
                dead_base = get_random_color()
            # Dim it to about 10% brightness
            self.dead_color = (dead_base[0] // 10, dead_base[1] // 10, dead_base[2] // 10)

        # Add random live cells (about 35-45% density for more action)
        density = 0.35 + random.randint(0, 10) * 0.01
        num_seeds = int(self.width * self.height * density)
        for _ in range(num_seeds):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.board[y][x] = 1

        self.stuck_counter = 0

    def _count_alive(self):
        """Count number of alive cells"""
        count = 0
        for row in self.board:
            count += sum(row)
        return count

    def _boards_equal(self, board1, board2):
        """Check if two boards are identical"""
        if board2 is None:
            return False
        for y in range(self.height):
            for x in range(self.width):
                if board1[y][x] != board2[y][x]:
                    return False
        return True

    def update(self):
        """Update game state and display"""
        # Check if a beat occurred this frame
        beat_now = self.clock and self.clock.beat_occurred()

        # Only advance simulation on each beat
        if beat_now:
            print("GOL: Beat detected, advancing simulation")
            # Check if board is stuck (no change) or dead
            alive_count = self._count_alive()
            is_stuck = self._boards_equal(self.board, self.prev_board)

            if alive_count == 0 or is_stuck:
                self.stuck_counter += 1
                if self.stuck_counter > 15:  # Reseed after being stuck for 15 beats
                    self._seed_random_pattern()
            else:
                self.stuck_counter = 0

            # Save current board before updating
            self.prev_board = [row[:] for row in self.board]

            # Update the board
            self.board = gol_step(self.board)

        # Draw to LEDs (every frame for smooth display)
        for y in range(self.height):
            for x in range(self.width):
                led_id = self.coords_to_id(x, y)
                if led_id is not None:
                    color = self.alive_color if self.board[y][x] == 1 else self.dead_color
                    self.pixels[led_id] = color

        return True
