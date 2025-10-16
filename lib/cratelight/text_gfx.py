"""GFX font rendering for LED displays using Adafruit bitmap fonts

Requires:
    - adafruit_bitmap_font (install via circup)

Usage:
    from cratelight.text_gfx import GFXTextRenderer
    from adafruit_bitmap_font import bitmap_font

    font = bitmap_font.load_font("/fonts/Arial-12.bdf")
    renderer = GFXTextRenderer(pixels, hardware_config, font)
    renderer.draw_text("Hello!", 0, 0, (255, 0, 0))
"""


class GFXTextRenderer:
    """
    Render text using Adafruit GFX bitmap fonts

    This renderer works with .bdf or .pcf bitmap fonts from Adafruit.
    Download fonts from: https://github.com/adafruit/Adafruit_CircuitPython_Bitmap_Font
    """

    def __init__(self, pixels, hardware_config, font):
        """
        Initialize GFX text renderer

        Args:
            pixels: NeoPixel object
            hardware_config: HardwareConfig object for coordinate mapping
            font: Loaded bitmap font from adafruit_bitmap_font
        """
        self.pixels = pixels
        self.config = hardware_config
        self.width = hardware_config.width
        self.height = hardware_config.height
        self.font = font

    def get_text_bounds(self, text):
        """
        Get the bounding box of text

        Args:
            text: String to measure

        Returns:
            (width, height) tuple in pixels
        """
        try:
            # Try the newer API first
            bbox = self.font.get_bounding_box()
            # Estimate based on character count
            char_width = bbox[0]
            char_height = bbox[1]
            width = len(text) * char_width
            height = char_height
        except AttributeError:
            # Fallback for older font API
            width = len(text) * 8  # Estimate
            height = 8

        return (width, height)

    def draw_text(self, text, x_pos, y_pos, fg_color, bg_color=(0, 0, 0)):
        """
        Draw text at specified position using GFX font

        Args:
            text: String to display
            x_pos: X position (left edge)
            y_pos: Y position (top edge, baseline of text)
            fg_color: Foreground color tuple (r, g, b)
            bg_color: Background color tuple (r, g, b)
        """
        # Get font's glyph data for each character
        current_x = x_pos

        for char in text:
            glyph = self.font.get_glyph(ord(char))
            if glyph is None:
                continue

            # Get glyph bitmap
            bitmap = glyph.bitmap
            if bitmap is None:
                current_x += glyph.shift_x
                continue

            # Render glyph to LED grid
            for gy in range(glyph.height):
                for gx in range(glyph.width):
                    # Calculate LED grid position
                    grid_x = current_x + gx + glyph.dx
                    grid_y = y_pos + gy + glyph.dy

                    # Check bounds
                    if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                        # Check if pixel is set in glyph bitmap
                        bit_index = gy * glyph.width + gx
                        byte_index = bit_index // 8
                        bit_offset = 7 - (bit_index % 8)

                        if byte_index < len(bitmap):
                            pixel_on = (bitmap[byte_index] >> bit_offset) & 1

                            led_id = self.config.coords_to_id(grid_x, grid_y)
                            if led_id is not None:
                                color = fg_color if pixel_on else bg_color
                                self.pixels[led_id] = color

            # Advance cursor
            current_x += glyph.shift_x

    def center_text(self, text, y_pos, fg_color, bg_color=(0, 0, 0)):
        """
        Draw text centered horizontally

        Args:
            text: String to display
            y_pos: Y position (baseline)
            fg_color: Foreground color tuple (r, g, b)
            bg_color: Background color tuple (r, g, b)
        """
        text_width, _ = self.get_text_bounds(text)
        x_pos = (self.width - text_width) // 2
        self.draw_text(text, x_pos, y_pos, fg_color, bg_color)

    def clear(self):
        """Clear all pixels"""
        for i in range(len(self.pixels)):
            self.pixels[i] = (0, 0, 0)


class SimpleGFXTextRenderer:
    """
    Simplified GFX text renderer that doesn't require adafruit_bitmap_font

    This is a fallback that uses a basic 8x8 monospace font built-in.
    For better fonts, use GFXTextRenderer with proper bitmap fonts.
    """

    # Simple 8x8 monospace font (uppercase letters only for demo)
    FONT_8x8 = {
        'A': [
            0b00111100,
            0b01000010,
            0b01000010,
            0b01111110,
            0b01000010,
            0b01000010,
            0b01000010,
            0b00000000,
        ],
        'B': [
            0b01111100,
            0b01000010,
            0b01000010,
            0b01111100,
            0b01000010,
            0b01000010,
            0b01111100,
            0b00000000,
        ],
        'C': [
            0b00111100,
            0b01000010,
            0b01000000,
            0b01000000,
            0b01000000,
            0b01000010,
            0b00111100,
            0b00000000,
        ],
        # Add more letters as needed...
        ' ': [0] * 8,
    }

    def __init__(self, pixels, hardware_config):
        """
        Initialize simple GFX text renderer

        Args:
            pixels: NeoPixel object
            hardware_config: HardwareConfig object for coordinate mapping
        """
        self.pixels = pixels
        self.config = hardware_config
        self.width = hardware_config.width
        self.height = hardware_config.height

    def draw_text(self, text, x_pos, y_pos, fg_color, bg_color=(0, 0, 0)):
        """
        Draw text using built-in 8x8 font

        Args:
            text: String to display
            x_pos: X position (left edge)
            y_pos: Y position (top edge)
            fg_color: Foreground color tuple (r, g, b)
            bg_color: Background color tuple (r, g, b)
        """
        current_x = x_pos

        for char in text.upper():
            if char not in self.FONT_8x8:
                char = ' '

            glyph = self.FONT_8x8[char]

            # Render each row of the character
            for gy, row_data in enumerate(glyph):
                for gx in range(8):
                    pixel_on = (row_data >> (7 - gx)) & 1

                    grid_x = current_x + gx
                    grid_y = y_pos + gy

                    # Check bounds
                    if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                        led_id = self.config.coords_to_id(grid_x, grid_y)
                        if led_id is not None:
                            color = fg_color if pixel_on else bg_color
                            self.pixels[led_id] = color

            current_x += 8  # Move to next character (8 pixels wide)

    def clear(self):
        """Clear all pixels"""
        for i in range(len(self.pixels)):
            self.pixels[i] = (0, 0, 0)
