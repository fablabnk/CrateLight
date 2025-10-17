"""Conway's Game of Life effect"""

import random
from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..utils import gol_step
from ..colors import COLORS

# Constants for Game of Life configuration
GOL_RAINBOW_HUE_STEP = 40  # Color change on each reseed
GOL_COMPLEMENTARY_OFFSET = 128  # Opposite color on wheel
GOL_BACKGROUND_BRIGHTNESS_DIVISOR = 7  # Dead cells at 1/7 brightness (15%)
GOL_MIN_DENSITY = 0.35  # Minimum starting cell density
GOL_DENSITY_VARIANCE = 0.10  # Random variance in density (0.35-0.45)
GOL_STUCK_THRESHOLD_BEATS = 15  # Beats before reseeding when stuck


class GameOfLife(Effect, BPMSyncedEffect):
    """Conway's Game of Life on LED grid"""

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None,
                 rainbow=False):
        """
        Initialize Game of Life

        Args:
            rainbow: If True, cycle through rainbow colors on each reseed
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
        # Randomize starting color in rainbow mode
        if self.rainbow:
            self.rainbow_offset = random.randint(0, 255)
        self._seed_random_pattern()

    def _seed_random_pattern(self):
        """Seed the board with random live cells"""
        # Clear board
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # Pick a random color for alive cells
        if self.rainbow:
            from ..utils import wheel
            self.alive_color = wheel(self.rainbow_offset)
            # Use complementary color (opposite on color wheel) for background
            complementary_offset = (self.rainbow_offset + GOL_COMPLEMENTARY_OFFSET) % 256
            base_dead = wheel(complementary_offset)
            # Dim the complementary color for subtle background
            self.dead_color = (base_dead[0] // GOL_BACKGROUND_BRIGHTNESS_DIVISOR,
                              base_dead[1] // GOL_BACKGROUND_BRIGHTNESS_DIVISOR,
                              base_dead[2] // GOL_BACKGROUND_BRIGHTNESS_DIVISOR)
            # Increment for next reseed
            self.rainbow_offset = (self.rainbow_offset + GOL_RAINBOW_HUE_STEP) % 256
        else:
            color_choices = [COLORS["RED"], COLORS["GREEN"], COLORS["BLUE"],
                            COLORS["YELLOW"], COLORS["CYAN"], COLORS["MAGENTA"],
                            COLORS["PURPLE"], COLORS["ORANGE"]]
            self.alive_color = random.choice(color_choices)

            # Always use a complementary background color (not just 30% of the time)
            dead_color_choices = [c for c in color_choices if c != self.alive_color]
            base_color = random.choice(dead_color_choices)
            # Dim it for visible but subtle background
            self.dead_color = (base_color[0] // GOL_BACKGROUND_BRIGHTNESS_DIVISOR,
                              base_color[1] // GOL_BACKGROUND_BRIGHTNESS_DIVISOR,
                              base_color[2] // GOL_BACKGROUND_BRIGHTNESS_DIVISOR)

        # Add random live cells with variable density for more action
        density = GOL_MIN_DENSITY + random.randint(0, int(GOL_DENSITY_VARIANCE * 100)) * 0.01
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
            # Check if board is stuck (no change) or dead
            alive_count = self._count_alive()
            is_stuck = self._boards_equal(self.board, self.prev_board)

            if alive_count == 0 or is_stuck:
                self.stuck_counter += 1
                if self.stuck_counter > GOL_STUCK_THRESHOLD_BEATS:
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

    def cleanup(self):
        """Clear display when effect ends"""
        self.pixels.fill(COLORS["OFF"])
