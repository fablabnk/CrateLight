"""Conway's Game of Life effect"""

import random
from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..utils import gol_step
from ..colors import COLORS


class GameOfLife(Effect, BPMSyncedEffect):
    """Conway's Game of Life on LED grid"""

    def setup(self):
        """Initialize the game board with random patterns"""
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.prev_board = None
        self.stuck_counter = 0
        self.dead_color = COLORS["OFF"]
        self._seed_random_pattern()

    def _seed_random_pattern(self):
        """Seed the board with random live cells"""
        # Clear board
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # Pick a random color for alive cells
        color_choices = [COLORS["RED"], COLORS["GREEN"], COLORS["BLUE"],
                        COLORS["YELLOW"], COLORS["CYAN"], COLORS["MAGENTA"],
                        COLORS["PURPLE"], COLORS["ORANGE"]]
        self.alive_color = random.choice(color_choices)

        # Pick a random color for dead cells (70% chance of OFF, 30% chance of dim color)
        if random.randint(0, 9) < 7:
            self.dead_color = COLORS["OFF"]
        else:
            # Use a different color from alive, dimmed down
            dead_color_choices = [c for c in color_choices if c != self.alive_color]
            base_color = random.choice(dead_color_choices)
            # Dim it to about 10% brightness
            self.dead_color = (base_color[0] // 10, base_color[1] // 10, base_color[2] // 10)

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
