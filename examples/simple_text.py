"""Simple text display example"""

import board
from cratelight import COLORS, LinearGrid, TextRenderer

# Setup hardware
config = LinearGrid(pin=board.GP2, width=32, height=8, brightness=0.2)
pixels = config.create_pixels()

# Create text renderer
text = TextRenderer(pixels, config)

# Display centered text
text.center_text("HELLO", y_pos=1, fg_color=COLORS["RED"])
pixels.show()

# Keep it on
input("Press Enter to clear...")

text.clear()
pixels.show()
