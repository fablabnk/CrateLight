"""Scrolling color effects"""

import random
from ..effect_base import Effect
from ..utils import wheel


class ColorScrollVertical(Effect):
    """Scroll rainbow colors vertically (up or down)"""

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None, direction=1):
        """
        Args:
            direction: 1 for up, -1 for down
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.direction = direction

    def setup(self):
        self.offset = 0

    def update(self):
        for y in range(self.height):
            # Calculate color based on position and offset
            color_pos = ((y * 15 + self.offset * 10 * self.direction) % 256)
            color = wheel(color_pos)

            # Fill entire row with this color
            for x in range(self.width):
                led_id = self.coords_to_id(x, y)
                if led_id is not None:
                    self.pixels[led_id] = color

        self.offset += 1
        return True  # Run indefinitely


class ColorScrollHorizontal(Effect):
    """Scroll colored bars horizontally (left or right)"""

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None, direction=1):
        """
        Args:
            direction: 1 for right, -1 for left
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.direction = direction

    def setup(self):
        self.offset = 0
        # Generate random colors for the bars
        self.colors = [
            (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            for _ in range(self.width * 2)
        ]

    def update(self):
        for x in range(self.width):
            # Get color from cycling color array
            color_idx = (x + self.offset * self.direction) % len(self.colors)
            color = self.colors[color_idx]

            # Fill entire column with this color
            for y in range(self.height):
                led_id = self.coords_to_id(x, y)
                if led_id is not None:
                    self.pixels[led_id] = color

        self.offset += 1
        return True  # Run indefinitely


class RainbowScroll(Effect):
    """
    Smooth rainbow scroll effect - works both horizontally and vertically

    Usage:
        manager.add_effect(RainbowScroll, beats=16, axis="horizontal", speed=1.5)
        manager.add_effect(RainbowScroll, beats=16, axis="vertical", speed=1.0, direction=-1)
    """

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None,
                 axis="horizontal", direction=1, speed=1.0):
        """
        Args:
            axis: "horizontal" or "vertical"
            direction: 1 for right/up, -1 for left/down
            speed: Scroll speed (fractional pixels per frame)
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.axis = axis.lower()
        self.direction = direction
        self.speed = speed

    def setup(self):
        self.offset = 0.0

    def update(self):
        # Fill entire grid
        for y in range(self.height):
            for x in range(self.width):
                if self.axis == "vertical":
                    # Vertical scroll - colors change by row
                    # Multiply by higher value for wider gradient spread
                    color_pos = int((y * 50 + self.offset * self.direction) % 256)
                else:
                    # Horizontal scroll - colors change by column
                    # Adjust multiplier based on grid width for good color distribution
                    color_pos = int((x * 12 + self.offset * self.direction) % 256)

                color = wheel(color_pos)
                led_id = self.coords_to_id(x, y)
                if led_id is not None:
                    self.pixels[led_id] = color

        self.offset += self.speed
        return True


# Backwards compatibility aliases
class RainbowScrollVertical(RainbowScroll):
    """Vertical rainbow scroll (legacy - use RainbowScroll with axis='vertical' instead)"""
    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None,
                 direction=1, speed=1.0):
        super().__init__(pixels, width, height, hardware_config, clock,
                        axis="vertical", direction=direction, speed=speed)


class RainbowScrollHorizontal(RainbowScroll):
    """Horizontal rainbow scroll (legacy - use RainbowScroll with axis='horizontal' instead)"""
    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None,
                 direction=1, speed=1.5):
        super().__init__(pixels, width, height, hardware_config, clock,
                        axis="horizontal", direction=direction, speed=speed)
