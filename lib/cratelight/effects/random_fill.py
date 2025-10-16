"""Random fill effects"""

import random
from ..effect_base import Effect


class RandomFill(Effect):
    """Fill entire matrix with random colors that change periodically"""

    def setup(self):
        self.change_interval = 5  # frames between color changes

    def update(self):
        if self.frame_count % self.change_interval == 0:
            # Generate random bright color
            color = (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            )

            # Fill all pixels with this color
            for i in range(len(self.pixels)):
                self.pixels[i] = color

        return True  # Run indefinitely


class PixelRandomFill(Effect):
    """Fill each pixel with random color one by one"""

    def setup(self):
        self.current_pixel = 0
        self.update_every = 1  # pixels to update per frame (higher = faster)

    def update(self):
        # Update multiple pixels per frame for speed
        for _ in range(self.update_every):
            if self.current_pixel < len(self.pixels):
                color = (
                    random.randint(50, 255),
                    random.randint(50, 255),
                    random.randint(50, 255)
                )
                self.pixels[self.current_pixel] = color
                self.current_pixel += 1
            else:
                # Hold the final pattern briefly before ending
                if self.frame_count > len(self.pixels) + 30:  # 1 second hold at 30fps
                    return False  # Effect complete

        return True


class RandomStrobe(Effect):
    """Random colored strobe/flash effect"""

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None, flashes=15):
        super().__init__(pixels, width, height, hardware_config, clock)
        self.flashes = flashes

    def setup(self):
        self.flash_count = 0
        self.is_on = False

    def update(self):
        if self.flash_count >= self.flashes * 2:  # *2 because on and off
            return False  # Effect complete

        if self.is_on:
            # Turn off
            for i in range(len(self.pixels)):
                self.pixels[i] = (0, 0, 0)
            self.is_on = False
            self.flash_count += 1
        else:
            # Turn on with random color
            color = (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            )
            for i in range(len(self.pixels)):
                self.pixels[i] = color
            self.is_on = True
            self.flash_count += 1

        return True
