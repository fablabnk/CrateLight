"""Knight Rider / scanner effects"""

import random
from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..colors import COLORS, get_random_color
from ..utils import wheel, scale_color

# Constants
KNIGHT_RIDER_CENTER_WIDTH = 2  # Width of bright center
KNIGHT_RIDER_TAIL_LENGTH = 6  # Length of trailing tail
KNIGHT_RIDER_BRIGHTNESS_CENTER = 1.0  # Brightness at center
KNIGHT_RIDER_BRIGHTNESS_MIN = 0.1  # Minimum tail brightness
KNIGHT_RIDER_RAINBOW_HUE_STEP = 20  # Color change per direction reversal


class KnightRiderEffect(Effect, BPMSyncedEffect):
    """
    Bright line sweeps back and forth with trailing tail - like KITT!
    Synced to beats for smooth, musical motion.

    Usage:
        manager.add_effect(KnightRiderEffect, beats=16, axis="horizontal", rainbow=True)
        manager.add_effect(KnightRiderEffect, beats=16, axis="vertical", color=COLORS["RED"])
        manager.add_effect(KnightRiderEffect, beats=16, axis="horizontal", random_color=True)
    """

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None,
                 axis="horizontal", rainbow=False, random_color=False, color=None):
        """
        Initialize Knight Rider effect

        Args:
            axis: "horizontal" (sweeps left/right) or "vertical" (sweeps up/down)
            rainbow: Cycle through rainbow colors on each direction change
            random_color: Random color on each direction change
            color: Fixed color (overrides other modes)
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.axis = axis
        self.rainbow = rainbow
        self.random_color = random_color
        self.fixed_color = color

    def setup(self):
        self.direction = 1  # 1 = forward, -1 = backward
        self.beat_count = 0
        self.rainbow_offset = 0

        # Pick color
        if self.fixed_color:
            self.current_color = self.fixed_color
        elif self.random_color:
            self.current_color = get_random_color()
        elif self.rainbow:
            self.current_color = wheel(self.rainbow_offset)
        else:
            self.current_color = COLORS["RED"]  # Classic KITT color!

    def update(self):
        # Track beats for direction changes
        if self.beat_occurred():
            self.beat_count += 1

        # Get phase within current beat (0.0 to 1.0)
        phase = self.get_beat_phase()

        # Calculate position based on axis and beat phase
        if self.axis == "horizontal":
            max_pos = self.width - 1
        else:  # vertical
            max_pos = self.height - 1

        # Every 2 beats, reverse direction and optionally change color
        beats_per_sweep = 2
        sweep_number = self.beat_count // beats_per_sweep
        current_direction = 1 if (sweep_number % 2 == 0) else -1

        # Change color on direction change
        if self.beat_count % beats_per_sweep == 0 and phase < 0.1:
            if self.random_color:
                self.current_color = get_random_color()
            elif self.rainbow:
                self.rainbow_offset = (self.rainbow_offset + KNIGHT_RIDER_RAINBOW_HUE_STEP) % 256
                self.current_color = wheel(self.rainbow_offset)

        # Calculate sweep position within this direction
        beats_into_sweep = self.beat_count % beats_per_sweep
        sweep_phase = (beats_into_sweep + phase) / beats_per_sweep

        if current_direction == 1:
            position = sweep_phase * max_pos
        else:
            position = (1.0 - sweep_phase) * max_pos

        # Clear all pixels
        self.pixels.fill(COLORS["OFF"])

        # Draw the scanner line with tail
        for y in range(self.height):
            for x in range(self.width):
                # Calculate distance from scanner position
                if self.axis == "horizontal":
                    distance = abs(x - position)
                else:  # vertical
                    distance = abs(y - position)

                # Calculate brightness based on distance
                if distance < KNIGHT_RIDER_CENTER_WIDTH:
                    brightness = KNIGHT_RIDER_BRIGHTNESS_CENTER
                elif distance < KNIGHT_RIDER_TAIL_LENGTH:
                    # Exponential falloff for tail
                    tail_pos = (distance - KNIGHT_RIDER_CENTER_WIDTH) / (KNIGHT_RIDER_TAIL_LENGTH - KNIGHT_RIDER_CENTER_WIDTH)
                    brightness = KNIGHT_RIDER_BRIGHTNESS_CENTER - (tail_pos ** 2) * (KNIGHT_RIDER_BRIGHTNESS_CENTER - KNIGHT_RIDER_BRIGHTNESS_MIN)
                else:
                    brightness = 0.0

                if brightness > KNIGHT_RIDER_BRIGHTNESS_MIN:
                    color = scale_color(self.current_color, brightness)
                    led_id = self.coords_to_id(x, y)
                    if led_id is not None:
                        self.pixels[led_id] = color

        return True

    def cleanup(self):
        """Clear display when effect ends"""
        self.pixels.fill(COLORS["OFF"])
