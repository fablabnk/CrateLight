"""Text rendering utilities for LED displays"""


class Font8x8:
    """8x8 pixel monospace font for LED displays"""

    # Standard 8x8 bitmap font - each character is 8 rows of 8 bits
    CHARS = {
        'A': [
            0b00111100,
            0b01000010,
            0b01000010,
            0b01111110,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
        ],
        'B': [
            0b01111100,
            0b01000010,
            0b01000010,
            0b01111100,
            0b01000010,
            0b01000010,
            0b01111100,
            0b01111000,
        ],
        'C': [
            0b00111100,
            0b01000010,
            0b01000000,
            0b01000000,
            0b01000000,
            0b01000010,
            0b00111100,
            0b00011000,
        ],
        'D': [
            0b01111000,
            0b01000100,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000100,
            0b01111000,
            0b01110000,
        ],
        'E': [
            0b01111110,
            0b01000000,
            0b01000000,
            0b01111100,
            0b01000000,
            0b01000000,
            0b01111110,
            0b01111110,
        ],
        'F': [
            0b01111110,
            0b01000000,
            0b01000000,
            0b01111100,
            0b01000000,
            0b01000000,
            0b01000000,
            0b01000000,
        ],
        'G': [
            0b00111100,
            0b01000010,
            0b01000000,
            0b01001110,
            0b01000010,
            0b01000010,
            0b00111100,
            0b00011000,
        ],
        'H': [
            0b01000010,
            0b01000010,
            0b01000010,
            0b01111110,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
        ],
        'I': [
            0b00111110,
            0b00001000,
            0b00001000,
            0b00001000,
            0b00001000,
            0b00001000,
            0b00001000,
            0b00111110,
        ],
        'J': [
            0b00011110,
            0b00000100,
            0b00000100,
            0b00000100,
            0b00000100,
            0b01000100,
            0b01000100,
            0b00111000,
        ],
        'K': [
            0b01000010,
            0b01000100,
            0b01001000,
            0b01110000,
            0b01001000,
            0b01000100,
            0b01000010,
            0b01000010,
        ],
        'L': [
            0b01000000,
            0b01000000,
            0b01000000,
            0b01000000,
            0b01000000,
            0b01000000,
            0b01000000,
            0b01111110,
        ],
        'M': [
            0b01000010,
            0b01100110,
            0b01011010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
        ],
        'N': [
            0b01000010,
            0b01100010,
            0b01010010,
            0b01001010,
            0b01000110,
            0b01000010,
            0b01000010,
            0b01000010,
        ],
        'O': [
            0b00111100,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b00111100,
        ],
        'P': [
            0b01111100,
            0b01000010,
            0b01000010,
            0b01111100,
            0b01000000,
            0b01000000,
            0b01000000,
            0b01000000,
        ],
        'Q': [
            0b00111100,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01001010,
            0b01000100,
            0b00111010,
        ],
        'R': [
            0b01111100,
            0b01000010,
            0b01000010,
            0b01111100,
            0b01001000,
            0b01000100,
            0b01000010,
            0b01000010,
        ],
        'S': [
            0b00111100,
            0b01000010,
            0b01000000,
            0b00111100,
            0b00000010,
            0b00000010,
            0b01000010,
            0b00111100,
        ],
        'T': [
            0b01111110,
            0b00001000,
            0b00001000,
            0b00001000,
            0b00001000,
            0b00001000,
            0b00001000,
            0b00001000,
        ],
        'U': [
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b00111100,
        ],
        'V': [
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b00100100,
            0b00011000,
        ],
        'W': [
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01000010,
            0b01011010,
            0b01100110,
            0b01000010,
        ],
        'X': [
            0b01000010,
            0b01000010,
            0b00100100,
            0b00011000,
            0b00100100,
            0b01000010,
            0b01000010,
            0b01000010,
        ],
        'Y': [
            0b01000010,
            0b01000010,
            0b00100100,
            0b00011000,
            0b00001000,
            0b00001000,
            0b00001000,
            0b00001000,
        ],
        'Z': [
            0b01111110,
            0b00000010,
            0b00000100,
            0b00011000,
            0b00011000,
            0b00100000,
            0b01000000,
            0b01111110,
        ],
        '0': [
            0b00111100,
            0b01000110,
            0b01001010,
            0b01010010,
            0b01100010,
            0b01000010,
            0b01000010,
            0b00111100,
        ],
        '1': [
            0b00001000,
            0b00011000,
            0b00001000,
            0b00001000,
            0b00001000,
            0b00001000,
            0b00011100,
            0b00000000,
        ],
        '2': [
            0b00111100,
            0b01000010,
            0b00000010,
            0b00001100,
            0b00110000,
            0b01000000,
            0b01111110,
            0b00000000,
        ],
        '3': [
            0b00111100,
            0b01000010,
            0b00000010,
            0b00011100,
            0b00000010,
            0b01000010,
            0b00111100,
            0b00000000,
        ],
        '4': [
            0b00000100,
            0b00001100,
            0b00010100,
            0b00100100,
            0b01111110,
            0b00000100,
            0b00000100,
            0b00000000,
        ],
        '5': [
            0b01111110,
            0b01000000,
            0b01111100,
            0b00000010,
            0b00000010,
            0b01000010,
            0b00111100,
            0b00000000,
        ],
        '6': [
            0b00011100,
            0b00100000,
            0b01000000,
            0b01111100,
            0b01000010,
            0b01000010,
            0b00111100,
            0b00000000,
        ],
        '7': [
            0b01111110,
            0b00000010,
            0b00000100,
            0b00001000,
            0b00010000,
            0b00010000,
            0b00010000,
            0b00000000,
        ],
        '8': [
            0b00111100,
            0b01000010,
            0b01000010,
            0b00111100,
            0b01000010,
            0b01000010,
            0b00111100,
            0b00000000,
        ],
        '9': [
            0b00111100,
            0b01000010,
            0b01000010,
            0b00111110,
            0b00000010,
            0b00000100,
            0b00111000,
            0b00000000,
        ],
        ' ': [0, 0, 0, 0, 0, 0, 0, 0],
        '!': [
            0b00001000,
            0b00001000,
            0b00001000,
            0b00001000,
            0b00000000,
            0b00001000,
            0b00001000,
            0b00000000,
        ],
        '?': [
            0b00111100,
            0b01000010,
            0b00000010,
            0b00001100,
            0b00001000,
            0b00000000,
            0b00001000,
            0b00000000,
        ],
        '.': [
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00011000,
            0b00011000,
            0b00000000,
        ],
        ',': [
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00011000,
            0b00001000,
            0b00010000,
        ],
        '-': [
            0b00000000,
            0b00000000,
            0b00000000,
            0b01111110,
            0b00000000,
            0b00000000,
            0b00000000,
            0b00000000,
        ],
        '+': [
            0b00000000,
            0b00001000,
            0b00001000,
            0b01111110,
            0b00001000,
            0b00001000,
            0b00000000,
            0b00000000,
        ],
        '=': [
            0b00000000,
            0b00000000,
            0b01111110,
            0b00000000,
            0b01111110,
            0b00000000,
            0b00000000,
            0b00000000,
        ],
        ':': [
            0b00000000,
            0b00011000,
            0b00011000,
            0b00000000,
            0b00011000,
            0b00011000,
            0b00000000,
            0b00000000,
        ],
        '/': [
            0b00000010,
            0b00000010,
            0b00000100,
            0b00001000,
            0b00010000,
            0b00100000,
            0b01000000,
            0b00000000,
        ],
        '*': [
            0b00000000,
            0b01000100,
            0b00101000,
            0b00010000,
            0b00101000,
            0b01000100,
            0b00000000,
            0b00000000,
        ],
        '<': [
            0b00000010,
            0b00000100,
            0b00001000,
            0b00010000,
            0b00001000,
            0b00000100,
            0b00000010,
            0b00000000,
        ],
        '>': [
            0b01000000,
            0b00100000,
            0b00010000,
            0b00001000,
            0b00010000,
            0b00100000,
            0b01000000,
            0b00000000,
        ],
    }

    CHAR_WIDTH = 8
    CHAR_HEIGHT = 8
    SPACING = 0  # No spacing needed for 8x8 monospace

    @staticmethod
    def get_char(char):
        """Get pixel data for a character (uppercase conversion)"""
        return Font8x8.CHARS.get(char.upper(), Font8x8.CHARS[' '])

    @staticmethod
    def text_width(text):
        """Calculate pixel width needed for text"""
        return len(text) * Font8x8.CHAR_WIDTH

    @staticmethod
    def render_text(text, bg_value=0):
        """
        Render text to a 2D array

        Args:
            text: String to render
            bg_value: Background value (0 or 1)

        Returns:
            2D array [y][x] where 1 = foreground, 0 = background
        """
        if not text:
            return [[]]

        width = Font8x8.text_width(text)
        height = Font8x8.CHAR_HEIGHT

        # Create empty canvas
        canvas = [[bg_value for _ in range(width)] for _ in range(height)]

        # Render each character
        x_offset = 0
        for char in text:
            char_data = Font8x8.get_char(char)

            for y in range(Font8x8.CHAR_HEIGHT):
                for x in range(Font8x8.CHAR_WIDTH):
                    if x_offset + x < width:
                        # Extract bit from byte
                        pixel_on = (char_data[y] >> (7 - x)) & 1
                        canvas[y][x_offset + x] = pixel_on

            x_offset += Font8x8.CHAR_WIDTH

        return canvas


class Font:
    """5x3 pixel font for LED displays"""

    CHARS = {
        'A': [[0, 1, 0], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 0, 1]],
        'B': [[1, 1, 0], [1, 0, 1], [1, 1, 0], [1, 0, 1], [1, 1, 0]],
        'C': [[0, 1, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 1]],
        'D': [[1, 1, 0], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 0]],
        'E': [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 1, 1]],
        'F': [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 0, 0]],
        'G': [[0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 0, 1], [0, 1, 1]],
        'H': [[1, 0, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 0, 1]],
        'I': [[1, 1, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0], [1, 1, 1]],
        'J': [[0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 1], [0, 1, 0]],
        'K': [[1, 0, 1], [1, 0, 1], [1, 1, 0], [1, 0, 1], [1, 0, 1]],
        'L': [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 1, 1]],
        'M': [[1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1]],
        'N': [[1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1]],
        'O': [[0, 1, 0], [1, 0, 1], [1, 0, 1], [1, 0, 1], [0, 1, 0]],
        'P': [[1, 1, 0], [1, 0, 1], [1, 1, 0], [1, 0, 0], [1, 0, 0]],
        'Q': [[0, 1, 0], [1, 0, 1], [1, 0, 1], [1, 0, 1], [0, 1, 1]],
        'R': [[1, 1, 0], [1, 0, 1], [1, 1, 0], [1, 0, 1], [1, 0, 1]],
        'S': [[0, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0]],
        'T': [[1, 1, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
        'U': [[1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [0, 1, 0]],
        'V': [[1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [0, 1, 0]],
        'W': [[1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 0]],
        'X': [[1, 0, 1], [1, 0, 1], [0, 1, 0], [1, 0, 1], [1, 0, 1]],
        'Y': [[1, 0, 1], [1, 0, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
        'Z': [[1, 1, 1], [0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 1]],
        '0': [[0, 1, 0], [1, 0, 1], [1, 0, 1], [1, 0, 1], [0, 1, 0]],
        '1': [[0, 1, 0], [1, 1, 0], [0, 1, 0], [0, 1, 0], [1, 1, 1]],
        '2': [[0, 1, 0], [1, 0, 1], [0, 0, 1], [0, 1, 0], [1, 1, 1]],
        '3': [[1, 1, 0], [0, 0, 1], [0, 1, 0], [0, 0, 1], [1, 1, 0]],
        '4': [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
        '5': [[1, 1, 1], [1, 0, 0], [1, 1, 0], [0, 0, 1], [1, 1, 0]],
        '6': [[0, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 1], [0, 1, 0]],
        '7': [[1, 1, 1], [0, 0, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
        '8': [[0, 1, 0], [1, 0, 1], [0, 1, 0], [1, 0, 1], [0, 1, 0]],
        '9': [[0, 1, 0], [1, 0, 1], [0, 1, 1], [0, 0, 1], [1, 1, 0]],
        '!': [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 0, 0], [0, 1, 0]],
        '?': [[0, 1, 0], [1, 0, 1], [0, 0, 1], [0, 1, 0], [0, 1, 0]],
        '.': [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 0]],
        ',': [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 0], [1, 0, 0]],
        ':': [[0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 1, 0], [0, 0, 0]],
        '-': [[0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 0, 0], [0, 0, 0]],
        '+': [[0, 0, 0], [0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 0, 0]],
        '=': [[0, 0, 0], [1, 1, 1], [0, 0, 0], [1, 1, 1], [0, 0, 0]],
        '<': [[0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]],
        '>': [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]],
        '*': [[0, 0, 0], [1, 0, 1], [0, 1, 0], [1, 0, 1], [0, 0, 0]],
        '/': [[0, 0, 1], [0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 0, 0]],
        ' ': [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
    }

    CHAR_WIDTH = 3
    CHAR_HEIGHT = 5
    SPACING = 1  # Pixels between characters

    @staticmethod
    def get_char(char):
        """Get pixel data for a character (uppercase conversion)"""
        return Font.CHARS.get(char.upper(), Font.CHARS[' '])

    @staticmethod
    def text_width(text):
        """Calculate pixel width needed for text"""
        if not text:
            return 0
        return len(text) * (Font.CHAR_WIDTH + Font.SPACING) - Font.SPACING

    @staticmethod
    def render_text(text, bg_value=0):
        """
        Render text to a 2D array

        Args:
            text: String to render
            bg_value: Background value (0 or 1)

        Returns:
            2D array [y][x] where 1 = foreground, 0 = background
        """
        if not text:
            return [[]]

        width = Font.text_width(text)
        height = Font.CHAR_HEIGHT

        # Create empty canvas
        canvas = [[bg_value for _ in range(width)] for _ in range(height)]

        # Render each character
        x_offset = 0
        for char in text:
            char_data = Font.get_char(char)

            for y in range(Font.CHAR_HEIGHT):
                for x in range(Font.CHAR_WIDTH):
                    if x_offset + x < width:
                        canvas[y][x_offset + x] = char_data[y][x]

            x_offset += Font.CHAR_WIDTH + Font.SPACING

        return canvas


class TextRenderer:
    """Helper class to render text on LED grids using hardware config"""

    def __init__(self, pixels, hardware_config, font=None):
        """
        Initialize text renderer

        Args:
            pixels: NeoPixel object
            hardware_config: HardwareConfig object for coordinate mapping
            font: Font class to use (Font or Font8x8), defaults to Font
        """
        self.pixels = pixels
        self.config = hardware_config
        self.width = hardware_config.width
        self.height = hardware_config.height
        self.font = font if font is not None else Font

    def draw_text(self, text, x_pos, y_pos, fg_color, bg_color=(0, 0, 0)):
        """
        Draw text at specified position

        Args:
            text: String to display
            x_pos: X position (left edge)
            y_pos: Y position (top edge)
            fg_color: Foreground color tuple (r, g, b)
            bg_color: Background color tuple (r, g, b)
        """
        text_data = self.font.render_text(text)

        for y in range(len(text_data)):
            for x in range(len(text_data[0])):
                grid_x = x_pos + x
                grid_y = y_pos + y

                # Check bounds
                if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                    led_id = self.config.coords_to_id(grid_x, grid_y)
                    if led_id is not None:
                        color = fg_color if text_data[y][x] else bg_color
                        self.pixels[led_id] = color

    def center_text(self, text, y_pos, fg_color, bg_color=(0, 0, 0)):
        """
        Draw text centered horizontally

        Args:
            text: String to display
            y_pos: Y position (top edge)
            fg_color: Foreground color tuple (r, g, b)
            bg_color: Background color tuple (r, g, b)
        """
        text_width = self.font.text_width(text)
        x_pos = (self.width - text_width) // 2
        self.draw_text(text, x_pos, y_pos, fg_color, bg_color)

    def clear(self):
        """Clear all pixels"""
        for i in range(len(self.pixels)):
            self.pixels[i] = (0, 0, 0)
