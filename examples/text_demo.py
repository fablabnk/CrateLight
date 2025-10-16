"""
Text Display Demo for CrateLight

Demonstrates various text effects with the dynamic hardware config system
"""

import board
from cratelight import COLORS, BPMClock, LinearGrid, EffectManager
from cratelight.effects import StaticText, ScrollingText, BlinkingText, CountdownEffect

# =====================================================
# Hardware Configuration
# =====================================================
# Works with ANY hardware config! Try different ones:

config = LinearGrid(pin=board.GP2, width=32, height=8, brightness=0.2)

# Or use:
# from cratelight import ZigzagGrid, CrateLightGrid
# config = ZigzagGrid(pin=board.GP2, width=32, height=8, brightness=0.2)
# config = CrateLightGrid(pin=board.GP28, brightness=0.5)

pixels = config.create_pixels()
clock = BPMClock(pin=board.GP15, default_bpm=120)

print(f"Text Demo - {config.width}x{config.height} LEDs")
print("Press Ctrl+C to stop\n")

# =====================================================
# Setup Effect Manager with Text Effects
# =====================================================
manager = EffectManager(pixels, config.width, config.height, config, clock)

# Static text - centered
manager.add_effect(StaticText, duration=3.0, text="HELLO",
                   color=COLORS["RED"], centered=True)

# Scrolling text - left
manager.add_effect(ScrollingText, duration=8.0, text="CRATELIGHT",
                   color=COLORS["CYAN"], speed=1, direction="left")

# Blinking alert
manager.add_effect(BlinkingText, duration=4.0, text="ALERT",
                   color=COLORS["ORANGE"], blink_speed=15)

# Countdown from 10
manager.add_effect(CountdownEffect, duration=11.0, start_value=10,
                   color=COLORS["GREEN"])

# Static message with custom position
manager.add_effect(StaticText, duration=3.0, text="BYE",
                   color=COLORS["PURPLE"], centered=True)

print("Text effects loaded!")

# =====================================================
# Run!
# =====================================================
try:
    manager.run(fps=30)
except KeyboardInterrupt:
    print("\nStopped!")
    pixels.fill(COLORS["OFF"])
    pixels.show()
