"""
CrateLight Quick Start Example

Just copy the 'lib' folder to your CircuitPython device and run this!
"""

import board
from cratelight import COLORS, FixedBPMClock, VerticalZigzagGrid
from cratelight.effect_manager import EffectManager
from cratelight.effects.color_scroll import (
    RainbowScrollHorizontal,
    RainbowScrollVertical,
)
from cratelight.effects.flash import FlashOnBeat, StrobeEffect
from cratelight.effects.gameoflife import GameOfLife
from cratelight.effects.pulse import PulseOnBeat
from cratelight.effects.rainbow import RainbowChase
from cratelight.effects.random_fill import RandomStrobe
from cratelight.effects.scrolling import ScrollingText
from cratelight.effects.wave import WaveEffect

# =====================================================
# Hardware Configuration
# =====================================================
# Change this to match your setup!

config = VerticalZigzagGrid(pin=board.GP2, width=32, height=8, brightness=0.1)

# For CrateLight 24x12 grid, use:
# from cratelight import CrateLightGrid:
# config = CrateLightGrid(pin=board.GP28, brightness=0.5)

# For simple LED strip, use:
# from cratelight import LEDStrip
# config = LEDStrip(pin=board.GP2, num_leds=256, brightness=0.1)

pixels = config.create_pixels()

# BPM Clock - Using FixedBPMClock for testing without hardware
# For hardware BPM input, use: clock = BPMClock(pin=board.GP15, default_bpm=120, output_pin=board.GP16)
clock = FixedBPMClock(bpm=140)

print(f"CrateLight Demo - {config.width}x{config.height} LEDs")
print(f"Using FixedBPMClock at {clock.get_bpm()} BPM")
print("Press Ctrl+C to stop\n")


# =====================================================
# Setup Effect Manager
# =====================================================
manager = EffectManager(pixels, config.width, config.height, config, clock)

# Add built-in effects with beat durations and colorful variations
manager.add_effect(
    ScrollingText, beats=16, text="FABLAB IS REAL COOL", random_color=True, speed=2
)
manager.add_effect(RainbowScrollHorizontal, beats=16, speed=1.5)  # Smooth horizontal scroll
manager.add_effect(StrobeEffect, beats=8, rainbow=True)
manager.add_effect(RainbowScrollVertical, beats=16, speed=1.0, direction=1)  # Scroll up slowly
manager.add_effect(FlashOnBeat, beats=8, rainbow=True)
manager.add_effect(RainbowChase, beats=12)
manager.add_effect(
    RainbowScrollHorizontal, beats=16, speed=0.8, direction=-1
)  # Scroll left slowly
manager.add_effect(PulseOnBeat, beats=12)  # Rainbow pulse
manager.add_effect(RainbowScrollVertical, beats=16, speed=1.2, direction=-1)  # Scroll down
manager.add_effect(GameOfLife, beats=20, rainbow=True)  # Rainbow Game of Life
manager.add_effect(StrobeEffect, beats=8, random_color=True)
manager.add_effect(RandomStrobe, duration=3, flashes=20)
manager.add_effect(RainbowScrollHorizontal, beats=16, speed=2.0)  # Faster horizontal
manager.add_effect(WaveEffect, beats=12)
manager.add_effect(GameOfLife, beats=20)  # Random colors Game of Life
manager.add_effect(FlashOnBeat, beats=8, random_color=True)
manager.add_effect(RainbowScrollVertical, beats=16, speed=1.8)  # Smooth vertical scroll
print("Effects loaded! Cycling through all effects...")
print(f"Running at {clock.get_bpm()} BPM\n")

# =====================================================
# Run!
# =====================================================
try:
    manager.run(fps=30)
except KeyboardInterrupt:
    print("\nStopped!")
    pixels.fill(COLORS["OFF"])
    pixels.show()
