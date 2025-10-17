"""Random fill effects"""

import random
from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..colors import COLORS, get_random_color


class RandomFill(Effect, BPMSyncedEffect):
    """Fill entire matrix with random colors that change on each beat"""

    def setup(self):
        self.current_color = get_random_color()

    def update(self):
        # Change color on each beat
        if self.beat_occurred():
            self.current_color = get_random_color()

        # Optimization: use fill() instead of loop
        self.pixels.fill(self.current_color)

        return True  # Run indefinitely

    def cleanup(self):
        """Clear display when effect ends"""
        self.pixels.fill(COLORS["OFF"])


class PixelRandomFill(Effect, BPMSyncedEffect):
    """Fill each pixel with random color, synced to beat phase"""

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None, beats=4):
        super().__init__(pixels, width, height, hardware_config, clock)
        self.total_beats = beats

    def setup(self):
        self.beat_count = 0
        self.num_leds = len(self.pixels)

    def update(self):
        # Track beats
        if self.beat_occurred():
            self.beat_count += 1
            if self.beat_count >= self.total_beats:
                return False  # Effect complete

        # Use beat phase to fill progressively
        phase = self.get_beat_phase()
        total_progress = (self.beat_count + phase) / self.total_beats
        pixels_to_fill = int(total_progress * self.num_leds)

        # Fill pixels up to current progress
        for i in range(self.num_leds):
            if i < pixels_to_fill:
                # Generate consistent color for this pixel (based on index)
                random.seed(i)  # Same seed = same color
                color = get_random_color()
                random.seed()  # Reset seed
                self.pixels[i] = color
            else:
                self.pixels[i] = COLORS["OFF"]

        return True

    def cleanup(self):
        """Clear display when effect ends"""
        self.pixels.fill(COLORS["OFF"])


class RandomStrobe(Effect, BPMSyncedEffect):
    """Random colored strobe that flashes ON BEAT"""

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None, beats=8):
        super().__init__(pixels, width, height, hardware_config, clock)
        self.total_beats = beats

    def setup(self):
        self.beat_count = 0
        self.current_color = get_random_color()

    def update(self):
        # Change color on each beat
        if self.beat_occurred():
            self.beat_count += 1
            self.current_color = get_random_color()

            # Stop after specified beats
            if self.beat_count >= self.total_beats:
                return False

        # Flash based on beat phase (on for first 20% of beat)
        phase = self.get_beat_phase()
        if phase < 0.2:
            self.pixels.fill(self.current_color)
        else:
            self.pixels.fill(COLORS["OFF"])

        return True

    def cleanup(self):
        """Clear display when effect ends"""
        self.pixels.fill(COLORS["OFF"])


class DirectionalFillOnBeat(Effect, BPMSyncedEffect):
    """
    Fill the grid from a direction ON each beat - like a wave sweeping across!

    Usage:
        manager.add_effect(DirectionalFillOnBeat, beats=8, direction="right", rainbow=True)
        manager.add_effect(DirectionalFillOnBeat, beats=8, direction="random", random_color=True)
    """

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None,
                 direction="right", rainbow=False, random_color=False, color=None):
        """
        Args:
            direction: "left", "right", "up", "down", or "random"
            rainbow: Cycle through rainbow colors
            random_color: Use random color each beat
            color: Fixed color (overrides other color modes)
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.direction = direction
        self.rainbow = rainbow
        self.random_color = random_color
        self.fixed_color = color

    def setup(self):
        self.current_color = COLORS["WHITE"]
        self.rainbow_offset = random.randint(0, 255) if self.rainbow else 0

        # Pick random direction if requested
        if self.direction == "random":
            self.active_direction = random.choice(["left", "right", "up", "down"])
        else:
            self.active_direction = self.direction

    def update(self):
        # Change color on beat
        if self.beat_occurred():
            if self.rainbow:
                from ..utils import wheel
                self.current_color = wheel(self.rainbow_offset)
                self.rainbow_offset = (self.rainbow_offset + 40) % 256
            elif self.random_color:
                self.current_color = get_random_color()
            elif self.fixed_color:
                self.current_color = self.fixed_color
            else:
                self.current_color = COLORS["WHITE"]

        # Use beat phase to create directional wipe effect
        phase = self.get_beat_phase()

        for y in range(self.height):
            for x in range(self.width):
                # Calculate if this pixel should be lit based on direction and phase
                if self.active_direction == "right":
                    progress = x / self.width
                elif self.active_direction == "left":
                    progress = (self.width - 1 - x) / self.width
                elif self.active_direction == "down":
                    progress = y / self.height
                else:  # up
                    progress = (self.height - 1 - y) / self.height

                # Light up pixel if phase has reached it
                if phase >= progress:
                    color = self.current_color
                else:
                    color = COLORS["OFF"]

                led_id = self.coords_to_id(x, y)
                if led_id is not None:
                    self.pixels[led_id] = color

        return True

    def cleanup(self):
        """Clear display when effect ends"""
        self.pixels.fill(COLORS["OFF"])
