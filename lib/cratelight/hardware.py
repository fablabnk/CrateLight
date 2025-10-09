"""Hardware configuration for different LED setups"""

import board
try:
    import adafruit_neopixel as neopixel
except ImportError:
    import neopixel


class HardwareConfig:
    """Base class for hardware configurations"""

    def __init__(self, pin, num_leds, brightness=0.5):
        self.pin = pin
        self.num_leds = num_leds
        self.brightness = brightness
        self.width = num_leds
        self.height = 1

    def coords_to_id(self, x, y):
        """Convert grid coordinates to LED ID - override in subclasses"""
        return x + (y * self.width)

    def id_to_coords(self, led_id):
        """Convert LED ID to coordinates - override in subclasses"""
        x = led_id % self.width
        y = led_id // self.width
        return (x, y)

    def create_pixels(self):
        """Create NeoPixel object with this configuration"""
        return neopixel.NeoPixel(
            self.pin,
            self.num_leds,
            brightness=self.brightness,
            auto_write=False
        )


class CrateLightGrid(HardwareConfig):
    """
    CrateLight 24x12 grid with custom wiring pattern

    Usage:
        config = CrateLightGrid(pin=board.GP28, brightness=0.5)
        pixels = config.create_pixels()
    """

    # Define your LED coordinate mapping
    IDS_BY_COORD = [
        [297, 298, 287, 286, 279, 278, 270, 269, 262, 261, 254, 253, 245, 244, 237, 236, 229, 228, 220, 219, 212, 211, 204, 203],
        [296, 295, 288, 285, 280, 277, 271, 268, 263, 260, 255, 252, 246, 243, 238, 235, 230, 227, 221, 218, 213, 210, 205, 202],
        [293, 294, 289, 284, 281, 276, 272, 267, 264, 259, 256, 251, 247, 242, 239, 234, 231, 226, 222, 217, 214, 209, 206, 201],
        [292, 291, 290, 283, 282, 275, 273, 266, 265, 258, 257, 250, 248, 241, 240, 233, 232, 225, 223, 216, 215, 208, 207, 200],
        [106, 107, 108, 115, 116, 123, 125, 132, 133, 140, 141, 148, 150, 157, 158, 165, 166, 173, 175, 182, 183, 190, 191, 198],
        [105, 104, 109, 114, 117, 122, 126, 131, 134, 139, 142, 147, 151, 156, 159, 164, 167, 172, 176, 181, 184, 189, 192, 197],
        [102, 103, 110, 113, 118, 121, 127, 130, 135, 138, 143, 146, 152, 155, 160, 163, 168, 171, 177, 180, 185, 188, 193, 196],
        [101, 100, 111, 112, 119, 120, 128, 129, 136, 137, 144, 145, 153, 154, 161, 162, 169, 170, 178, 179, 186, 187, 194, 195],
        [97, 98, 87, 86, 79, 78, 70, 69, 62, 61, 54, 53, 45, 44, 37, 36, 29, 28, 20, 19, 12, 11, 4, 3],
        [96, 95, 88, 85, 80, 77, 71, 68, 63, 60, 55, 52, 46, 43, 38, 35, 30, 27, 21, 18, 13, 10, 5, 2],
        [93, 94, 89, 84, 81, 76, 72, 67, 64, 59, 56, 51, 47, 42, 39, 34, 31, 26, 22, 17, 14, 9, 6, 1],
        [92, 91, 90, 83, 82, 75, 73, 66, 65, 58, 57, 50, 48, 41, 40, 33, 32, 25, 23, 16, 15, 8, 7, 0]
    ]

    def __init__(self, pin=board.GP28, brightness=0.5):
        super().__init__(pin, num_leds=300, brightness=brightness)
        self.width = 24
        self.height = 12

    def coords_to_id(self, x, y):
        """Convert grid coordinates (x, y) to LED ID"""
        try:
            return self.IDS_BY_COORD[y][x]
        except IndexError:
            return None

    def id_to_coords(self, led_id):
        """Convert LED ID to grid coordinates (x, y)"""
        for y, row in enumerate(self.IDS_BY_COORD):
            for x, id in enumerate(row):
                if id == led_id:
                    return (x, y)
        return None


class LEDStrip(HardwareConfig):
    """
    Simple LED strip - linear mapping

    Usage:
        config = LEDStrip(pin=board.GP2, num_leds=256, brightness=0.1)
        pixels = config.create_pixels()
    """

    def __init__(self, pin=board.GP2, num_leds=256, brightness=0.1):
        super().__init__(pin, num_leds, brightness)
        self.width = num_leds
        self.height = 1

    def coords_to_id(self, x, y):
        """Simple linear mapping for strip"""
        if 0 <= x < self.num_leds and y == 0:
            return x
        return None

    def id_to_coords(self, led_id):
        """Simple linear mapping for strip"""
        if 0 <= led_id < self.num_leds:
            return (led_id, 0)
        return None


class ZigzagGrid(HardwareConfig):
    """
    Grid with zigzag wiring pattern (common for LED matrices)

    Even rows go left-to-right, odd rows go right-to-left

    Usage:
        config = ZigzagGrid(pin=board.GP2, width=32, height=8, brightness=0.1)
        pixels = config.create_pixels()
    """

    def __init__(self, pin=board.GP2, width=32, height=8, brightness=0.1):
        super().__init__(pin, num_leds=width * height, brightness=brightness)
        self.width = width
        self.height = height

    def coords_to_id(self, x, y):
        """Zigzag pattern mapping"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return None

        if y % 2 == 0:  # Even rows: left to right
            return y * self.width + x
        else:  # Odd rows: right to left
            return y * self.width + (self.width - 1 - x)

    def id_to_coords(self, led_id):
        """Reverse zigzag pattern mapping"""
        if not (0 <= led_id < self.num_leds):
            return None

        y = led_id // self.width
        if y % 2 == 0:  # Even rows: left to right
            x = led_id % self.width
        else:  # Odd rows: right to left
            x = self.width - 1 - (led_id % self.width)

        return (x, y)


class LinearGrid(HardwareConfig):
    """
    Simple linear grid (row-by-row, left-to-right)

    Usage:
        config = LinearGrid(pin=board.GP2, width=32, height=8, brightness=0.1)
        pixels = config.create_pixels()
    """

    def __init__(self, pin=board.GP2, width=32, height=8, brightness=0.1):
        super().__init__(pin, num_leds=width * height, brightness=brightness)
        self.width = width
        self.height = height

    def coords_to_id(self, x, y):
        """Simple row-major mapping"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return y * self.width + x
        return None

    def id_to_coords(self, led_id):
        """Simple row-major mapping"""
        if 0 <= led_id < self.num_leds:
            x = led_id % self.width
            y = led_id // self.width
            return (x, y)
        return None
