"""Base class for creating custom LED effects"""

import time

class Effect:
    """
    Base class for all LED effects.

    To create a custom effect:
    1. Inherit from this class
    2. Implement the setup() method for initialization
    3. Implement the update() method for each animation frame
    4. Optionally implement cleanup() for teardown

    Example:
        class MyEffect(Effect):
            def setup(self):
                self.counter = 0

            def update(self):
                # Your animation logic here
                self.counter += 1
                return self.counter < 100  # Return False to stop
    """

    def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None):
        """
        Initialize the effect

        Args:
            pixels: NeoPixel object to control LEDs
            width: Grid width (default 24)
            height: Grid height (default 12)
            hardware_config: Optional HardwareConfig object for coordinate mapping
            clock: Optional clock source (BPMClock, FixedBPMClock, etc.)
        """
        self.pixels = pixels
        self.width = width
        self.height = height
        self.hardware_config = hardware_config
        self.clock = clock
        self.frame_count = 0

    def coords_to_id(self, x, y):
        """
        Convert grid coordinates to LED ID

        Uses hardware_config if provided, otherwise simple linear mapping
        """
        if self.hardware_config:
            return self.hardware_config.coords_to_id(x, y)
        else:
            # Default simple mapping
            if 0 <= x < self.width and 0 <= y < self.height:
                return y * self.width + x
            return None

    def id_to_coords(self, led_id):
        """
        Convert LED ID to grid coordinates

        Uses hardware_config if provided, otherwise simple linear mapping
        """
        if self.hardware_config:
            return self.hardware_config.id_to_coords(led_id)
        else:
            # Default simple mapping
            num_leds = self.width * self.height
            if 0 <= led_id < num_leds:
                x = led_id % self.width
                y = led_id // self.width
                return (x, y)
            return None

    def setup(self):
        """
        Called once before the effect starts.
        Use this to initialize variables, colors, patterns, etc.
        Override this in your effect class.
        """
        pass

    def update(self):
        """
        Called every frame to update the LED display.
        Override this in your effect class.

        Returns:
            bool: True to continue running, False to stop the effect
        """
        raise NotImplementedError("Effect must implement update() method")

    def cleanup(self):
        """
        Called once after the effect ends.
        Use this to clean up resources or reset the display.
        """
        pass

    def run(self, fps=30, max_frames=None):
        """
        Run the effect

        Args:
            fps: Frames per second (default 30)
            max_frames: Maximum frames to run, None for infinite
        """
        self.setup()
        frame_delay = 1.0 / fps

        try:
            while True:
                if max_frames and self.frame_count >= max_frames:
                    break

                should_continue = self.update()
                self.pixels.show()
                self.frame_count += 1

                if should_continue is False:
                    break

                time.sleep(frame_delay)
        finally:
            self.cleanup()
