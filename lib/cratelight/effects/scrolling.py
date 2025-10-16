"""Text display effects for LED grids"""

from cratelight import Effect, COLORS, get_random_color
from cratelight.text import Font, Font8x8, TextRenderer


class StaticText(Effect):
    """
    Display static text on the LED grid

    Usage:
        manager.add_effect(StaticText, duration=5.0, text="HELLO",
                          color=COLORS["RED"], centered=True)
    """

    def __init__(self, pixels, width, height, hardware_config, clock=None,
                 text="HELLO", color=COLORS["WHITE"], bg_color=COLORS["OFF"],
                 x=None, y=None, centered=True, font=None):
        """
        Initialize static text effect

        Args:
            text: Text to display
            color: Text color
            bg_color: Background color
            x: X position (left edge), None for centered
            y: Y position (top edge), defaults to vertical center
            centered: Center text horizontally (overrides x)
            font: Font class to use (Font or Font8x8), defaults to Font
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.x = x
        self.font = font if font is not None else Font
        self.y = y if y is not None else (height - self.font.CHAR_HEIGHT) // 2
        self.centered = centered
        self.renderer = TextRenderer(pixels, hardware_config, self.font)

    def setup(self):
        """Initialize text display"""
        self.renderer.clear()

    def update(self):
        """Display text"""
        if self.centered or self.x is None:
            self.renderer.center_text(self.text, self.y, self.color, self.bg_color)
        else:
            self.renderer.draw_text(self.text, self.x, self.y, self.color, self.bg_color)
        return True

    def cleanup(self):
        """Clear display"""
        self.renderer.clear()


class ScrollingText(Effect):
    """
    Scroll text across the LED grid

    Usage:
        manager.add_effect(ScrollingText, beats=16, text="HELLO WORLD",
                          color=COLORS["CYAN"], speed=2)
    """

    def __init__(self, pixels, width, height, hardware_config, clock=None,
                 text="HELLO", color=COLORS["WHITE"], bg_color=COLORS["OFF"],
                 y=None, speed=2, direction="left", random_color=False, font=None):
        """
        Initialize scrolling text effect

        Args:
            text: Text to display
            color: Text color
            bg_color: Background color
            y: Y position (top edge), defaults to vertical center
            speed: Pixels to move per frame
            direction: "left" or "right"
            random_color: Change color on each loop
            font: Font class to use (Font or Font8x8), defaults to Font
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.font = font if font is not None else Font
        self.y = y if y is not None else (height - self.font.CHAR_HEIGHT) // 2
        self.speed = speed
        self.direction = direction
        self.renderer = TextRenderer(pixels, hardware_config, self.font)
        self.x_pos = 0
        self.text_width = self.font.text_width(text)
        self.random_color = random_color

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


class BlinkingText(Effect):
    """
    Display blinking text

    Usage:
        manager.add_effect(BlinkingText, duration=5.0, text="ALERT",
                          color=COLORS["RED"], blink_speed=10)
    """

    def __init__(self, pixels, width, height, hardware_config, clock=None,
                 text="BLINK", color=COLORS["WHITE"], bg_color=COLORS["OFF"],
                 x=None, y=None, centered=True, blink_speed=15, font=None):
        """
        Initialize blinking text effect

        Args:
            text: Text to display
            color: Text color
            bg_color: Background color
            x: X position (left edge), None for centered
            y: Y position (top edge), defaults to vertical center
            centered: Center text horizontally
            blink_speed: Frames between blinks
            font: Font class to use (Font or Font8x8), defaults to Font
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.x = x
        self.font = font if font is not None else Font
        self.y = y if y is not None else (height - self.font.CHAR_HEIGHT) // 2
        self.centered = centered
        self.blink_speed = blink_speed
        self.renderer = TextRenderer(pixels, hardware_config, self.font)
        self.visible = True

    def setup(self):
        """Initialize blink state"""
        self.visible = True

    def update(self):
        """Toggle text visibility"""
        # Toggle visibility
        if self.frame_count % self.blink_speed == 0:
            self.visible = not self.visible

        # Draw text or clear based on visibility
        if self.visible:
            if self.centered or self.x is None:
                self.renderer.center_text(self.text, self.y, self.color, self.bg_color)
            else:
                self.renderer.draw_text(self.text, self.x, self.y, self.color, self.bg_color)
        else:
            self.renderer.clear()

        return True

    def cleanup(self):
        """Clear display"""
        self.renderer.clear()


class CountdownEffect(Effect):
    """
    Display a countdown timer

    Usage:
        manager.add_effect(CountdownEffect, duration=10.0, start_value=10,
                          color=COLORS["GREEN"])
    """

    def __init__(self, pixels, width, height, hardware_config, clock=None,
                 start_value=10, color=COLORS["WHITE"], bg_color=COLORS["OFF"],
                 centered=True, update_speed=30, font=None):
        """
        Initialize countdown effect

        Args:
            start_value: Starting number
            color: Text color
            bg_color: Background color
            centered: Center text horizontally
            update_speed: Frames between countdown updates
            font: Font class to use (Font or Font8x8), defaults to Font
        """
        super().__init__(pixels, width, height, hardware_config, clock)
        self.start_value = start_value
        self.current_value = start_value
        self.color = color
        self.bg_color = bg_color
        self.centered = centered
        self.update_speed = update_speed
        self.font = font if font is not None else Font
        self.y = (height - self.font.CHAR_HEIGHT) // 2
        self.renderer = TextRenderer(pixels, hardware_config, self.font)

    def setup(self):
        """Initialize countdown"""
        self.current_value = self.start_value

    def update(self):
        """Update countdown"""
        # Update value
        if self.frame_count % self.update_speed == 0 and self.frame_count > 0:
            self.current_value -= 1

        # Draw current value
        text = str(self.current_value)
        if self.centered:
            self.renderer.center_text(text, self.y, self.color, self.bg_color)
        else:
            self.renderer.draw_text(text, 0, self.y, self.color, self.bg_color)

        # Stop when reaching 0
        return self.current_value >= 0

    def cleanup(self):
        """Clear display"""
        self.renderer.clear()
