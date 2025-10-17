"""Concentric ring and ripple effects"""

import random
from ..effect_base import Effect
from ..effect_manager import BPMSyncedEffect
from ..colors import COLORS, get_random_color
from ..utils import wheel, scale_color

# Constants
RINGS_RING_WIDTH = 1.5  # Width of each ring
RINGS_FADE_DISTANCE = 3.0  # Distance over which rings fade
RINGS_BRIGHTNESS_MAX = 1.0  # Maximum brightness
RINGS_BRIGHTNESS_MIN = 0.1  # Minimum brightness
RINGS_RAINBOW_HUE_STEP = 40  # Color change per beat


class ConcentricRingsEffect(Effect, BPMSyncedEffect):
    """
    Rings expand from origin point on each beat with trailing fade.
    Like ripples in water, synced to the music!

    Usage:
        manager.add_effect(ConcentricRingsEffect, beats=16, origin="center", rainbow=True)
        manager.add_effect(ConcentricRingsEffect, beats=16, origin="random", random_color=True)
        manager.add_effect(ConcentricRingsEffect, beats=16, origin="corners", color=COLORS["BLUE"])
    """

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None,
                 origin="center", rainbow=False, random_color=False, color=None):
        """
        Initialize concentric rings effect

        Args:
            origin: "center", "corners", "random", or "edges"
            rainbow: Cycle through rainbow colors
            random_color: Random color per beat
            color: Fixed color (overrides other modes)
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.origin_mode = origin
        self.rainbow = rainbow
        self.random_color = random_color
        self.fixed_color = color

    def setup(self):
        self.beat_count = 0
        self.rainbow_offset = random.randint(0, 255) if self.rainbow else 0

        # Set origin point(s)
        self._set_origin()

        # Pick initial color
        if self.fixed_color:
            self.current_color = self.fixed_color
        elif self.random_color:
            self.current_color = get_random_color()
        elif self.rainbow:
            self.current_color = wheel(self.rainbow_offset)
        else:
            self.current_color = COLORS["WHITE"]

    def _set_origin(self):
        """Set origin point(s) based on mode"""
        if self.origin_mode == "center":
            self.origins = [(self.width / 2.0, self.height / 2.0)]
        elif self.origin_mode == "corners":
            self.origins = [
                (0, 0),
                (self.width - 1, 0),
                (0, self.height - 1),
                (self.width - 1, self.height - 1)
            ]
        elif self.origin_mode == "edges":
            # Top, bottom, left, right midpoints
            self.origins = [
                (self.width / 2.0, 0),
                (self.width / 2.0, self.height - 1),
                (0, self.height / 2.0),
                (self.width - 1, self.height / 2.0)
            ]
        elif self.origin_mode == "random":
            # Pick new random origin
            self.origins = [(random.uniform(0, self.width), random.uniform(0, self.height))]
        else:
            # Default to center
            self.origins = [(self.width / 2.0, self.height / 2.0)]

    def update(self):
        # Change color and optionally origin on beat
        if self.beat_occurred():
            self.beat_count += 1

            # Change origin if random mode
            if self.origin_mode == "random":
                self._set_origin()

            # Change color
            if self.random_color:
                self.current_color = get_random_color()
            elif self.rainbow:
                self.rainbow_offset = (self.rainbow_offset + RINGS_RAINBOW_HUE_STEP) % 256
                self.current_color = wheel(self.rainbow_offset)

        # Get phase for expansion
        phase = self.get_beat_phase()

        # Calculate max possible distance (diagonal of grid)
        max_distance = ((self.width ** 2) + (self.height ** 2)) ** 0.5

        # Expansion radius for this beat
        expansion_radius = phase * max_distance

        # Clear display
        self.pixels.fill(COLORS["OFF"])

        # Draw rings from each origin
        for y in range(self.height):
            for x in range(self.width):
                brightest = 0.0

                # Check distance from all origins
                for origin_x, origin_y in self.origins:
                    # Calculate distance from this origin
                    dx = x - origin_x
                    dy = y - origin_y
                    distance = (dx ** 2 + dy ** 2) ** 0.5

                    # Calculate how far from the expanding ring edge
                    distance_from_ring = abs(distance - expansion_radius)

                    # Calculate brightness based on distance from ring
                    if distance_from_ring < RINGS_RING_WIDTH:
                        # On the ring
                        brightness = RINGS_BRIGHTNESS_MAX
                    elif distance_from_ring < RINGS_RING_WIDTH + RINGS_FADE_DISTANCE:
                        # In fade zone
                        fade_pos = (distance_from_ring - RINGS_RING_WIDTH) / RINGS_FADE_DISTANCE
                        brightness = RINGS_BRIGHTNESS_MAX - (fade_pos * (RINGS_BRIGHTNESS_MAX - RINGS_BRIGHTNESS_MIN))
                    else:
                        brightness = 0.0

                    # Keep brightest value if multiple origins
                    brightest = max(brightest, brightness)

                # Set pixel if bright enough
                if brightest > RINGS_BRIGHTNESS_MIN:
                    color = scale_color(self.current_color, brightest)
                    led_id = self.coords_to_id(x, y)
                    if led_id is not None:
                        self.pixels[led_id] = color

        return True

    def cleanup(self):
        """Clear display when effect ends"""
        self.pixels.fill(COLORS["OFF"])
