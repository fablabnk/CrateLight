"""GFX font scrolling text effects for LED grids

These effects use Adafruit bitmap fonts for larger, more readable text.

Requires:
    - adafruit_bitmap_font library (optional, fallback available)

Usage:
    from adafruit_bitmap_font import bitmap_font

    # Load a font
    font = bitmap_font.load_font("/fonts/Arial-16.bdf")

    # Use with effect manager
    manager.add_effect(
        GFXScrollingText,
        beats=16,
        text="HELLO WORLD",
        font=font,
        color=COLORS["CYAN"]
    )
"""

from cratelight import Effect, COLORS, get_random_color

try:
    from ..text_gfx import GFXTextRenderer, SimpleGFXTextRenderer
    HAS_GFX = True
except ImportError:
    HAS_GFX = False


class GFXScrollingText(Effect):
    """
    Scrolling text effect using GFX bitmap fonts

    This provides much better readability than the tiny 5x3 bitmap font.
    You can use any .bdf or .pcf bitmap font from Adafruit.

    Usage:
        # With custom font
        from adafruit_bitmap_font import bitmap_font
        font = bitmap_font.load_font("/fonts/Arial-12.bdf")
        manager.add_effect(GFXScrollingText, beats=16, text="HI!", font=font)

        # With built-in simple font (no adafruit_bitmap_font needed)
        manager.add_effect(GFXScrollingText, beats=16, text="HI!", font=None)
    """

    def __init__(self, pixels, width, height, hardware_config, clock=None,
                 text="HELLO", font=None, color=COLORS["WHITE"], bg_color=COLORS["OFF"],
                 y=None, speed=1, direction="left", random_color=False):
        """
        Initialize GFX scrolling text effect

        Args:
            text: Text to display
            font: Loaded bitmap font (or None for simple built-in font)
            color: Text color
            bg_color: Background color
            y: Y position (baseline), defaults to vertical center
            speed: Scroll speed in pixels per frame
            direction: "left" or "right"
            random_color: Change color on each loop
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.speed = speed
        self.direction = direction
        self.random_color = random_color

        # Create appropriate renderer
        if font is not None and HAS_GFX:
            from ..text_gfx import GFXTextRenderer
            self.renderer = GFXTextRenderer(pixels, hardware_config, font)
            text_width, text_height = self.renderer.get_text_bounds(text)
        elif HAS_GFX:
            from ..text_gfx import SimpleGFXTextRenderer
            self.renderer = SimpleGFXTextRenderer(pixels, hardware_config)
            text_width = len(text) * 8
            text_height = 8
        else:
            raise ImportError("text_gfx module not available")

        self.text_width = text_width
        self.text_height = text_height

        # Set Y position (baseline for GFX fonts)
        if y is None:
            self.y = (height + text_height) // 2
        else:
            self.y = y

    def setup(self):
        """Initialize scroll position"""
        if self.direction == "left":
            self.x_pos = self.width
        else:
            self.x_pos = -self.text_width

        # Start with random color if enabled
        if self.random_color:
            self.color = get_random_color()

    def update(self):
        """Scroll text"""
        # Clear and draw
        self.renderer.clear()
        self.renderer.draw_text(self.text, int(self.x_pos), self.y,
                               self.color, self.bg_color)

        # Update position
        if self.direction == "left":
            self.x_pos -= self.speed
            # Check if text has scrolled off screen
            if self.x_pos + self.text_width < 0:
                self.x_pos = self.width  # Wrap around
                if self.random_color:
                    self.color = get_random_color()
        else:
            self.x_pos += self.speed
            # Check if text has scrolled off screen
            if self.x_pos > self.width:
                self.x_pos = -self.text_width  # Wrap around
                if self.random_color:
                    self.color = get_random_color()

        return True

    def cleanup(self):
        """Clear display"""
        self.renderer.clear()


class GFXStaticText(Effect):
    """
    Static text display using GFX fonts

    Usage:
        from adafruit_bitmap_font import bitmap_font
        font = bitmap_font.load_font("/fonts/Arial-Bold-16.bdf")
        manager.add_effect(
            GFXStaticText,
            duration=5,
            text="STOP",
            font=font,
            color=COLORS["RED"]
        )
    """

    def __init__(self, pixels, width, height, hardware_config, clock=None,
                 text="HELLO", font=None, color=COLORS["WHITE"], bg_color=COLORS["OFF"],
                 x=None, y=None, centered=True):
        """
        Initialize static GFX text

        Args:
            text: Text to display
            font: Loaded bitmap font (or None for simple built-in font)
            color: Text color
            bg_color: Background color
            x: X position (left edge), ignored if centered=True
            y: Y position (baseline)
            centered: Center text horizontally
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.centered = centered

        # Create appropriate renderer
        if font is not None and HAS_GFX:
            from ..text_gfx import GFXTextRenderer
            self.renderer = GFXTextRenderer(pixels, hardware_config, font)
            text_width, text_height = self.renderer.get_text_bounds(text)
        elif HAS_GFX:
            from ..text_gfx import SimpleGFXTextRenderer
            self.renderer = SimpleGFXTextRenderer(pixels, hardware_config)
            text_width = len(text) * 8
            text_height = 8
        else:
            raise ImportError("text_gfx module not available")

        # Set position
        if centered:
            self.x = (width - text_width) // 2
        else:
            self.x = x if x is not None else 0

        if y is None:
            self.y = (height + text_height) // 2
        else:
            self.y = y

    def setup(self):
        """Initialize"""
        pass

    def update(self):
        """Display static text"""
        self.renderer.draw_text(self.text, self.x, self.y,
                               self.color, self.bg_color)
        return True

    def cleanup(self):
        """Clear display"""
        self.renderer.clear()
