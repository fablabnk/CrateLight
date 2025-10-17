"""
Custom Effect Template

Copy this file to create your own LED effects for CrateLight.
Replace the class name and implement your animation logic.
"""

import sys
sys.path.insert(0, '../lib')

import board
from cratelight import Effect, COLORS, CrateLightGrid
from cratelight.effect_manager import BPMSyncedEffect


class MyCustomEffect(Effect, BPMSyncedEffect):
    """
    Description of what your effect does

    Usage:
        manager.add_effect(MyCustomEffect, beats=8, param=value)
    """

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None):
        """
        Initialize your effect

        Args:
            pixels: NeoPixel object
            width: Grid width
            height: Grid height
            hardware_config: Hardware configuration object
            clock: Optional BPM clock for synchronization
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        # Add any custom parameters here

    def setup(self):
        """
        Initialize your effect state - called once when effect starts
        """
        # Initialize variables
        self.frame = 0
        # Example: self.color = COLORS["RED"]
        pass

    def update(self):
        """
        Run each frame - return True to continue, False to stop

        This method is called repeatedly at the specified FPS.
        Update your LED states here.
        """
        # Example: Light up LEDs based on frame count
        # for i in range(len(self.pixels)):
        #     self.pixels[i] = COLORS["BLUE"]

        self.frame += 1

        # Return True to keep running, False to stop
        return True

    def cleanup(self):
        """
        Optional cleanup when effect ends
        """
        # Turn off all LEDs
        self.pixels.fill(COLORS["OFF"])


# Example usage
if __name__ == "__main__":
    # 1. Configure hardware
    config = CrateLightGrid(pin=board.GP28, brightness=0.5)
    pixels = config.create_pixels()

    # 2. Create and run effect
    effect = MyCustomEffect(pixels, config.width, config.height, config)
    effect.run(fps=30)
