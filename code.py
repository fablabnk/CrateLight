"""
CrateLight Quick Start Example

Just copy the 'lib' folder to your CircuitPython device and run this!
"""

import board
from cratelight import COLORS, BPMClock, LinearGrid
from cratelight.effect_manager import EffectManager
from cratelight.effects.flash import FlashOnBeat
from cratelight.effects.gameoflife import GameOfLife
from cratelight.effects.pulse import PulseOnBeat
from cratelight.effects.rainbow import RainbowChase
from cratelight.effects.wave import WaveEffect

# =====================================================
# Hardware Configuration
# =====================================================
# Change this to match your setup!

config = LinearGrid(pin=board.GP2, width=32, height=8, brightness=0.1)

# For CrateLight 24x12 grid, use:
# from cratelight import CrateLightGrid:
# config = CrateLightGrid(pin=board.GP28, brightness=0.5)

# For simple LED strip, use:
# from cratelight import LEDStrip
# config = LEDStrip(pin=board.GP2, num_leds=256, brightness=0.1)

pixels = config.create_pixels()

# BPM Clock (optional - for synced effects)
clock = BPMClock(pin=board.GP15, default_bpm=120, output_pin=board.GP16)

print(f"CrateLight Demo - {config.width}x{config.height} LEDs")
print("BPM Input: GP15, Output: GP16")
print("Press Ctrl+C to stop\n")


# =====================================================
# Setup Effect Manager
# =====================================================
manager = EffectManager(pixels, config.width, config.height, config, clock)

# Add built-in effects with beat durations
# manager.add_effect(PulseOnBeat, beats=8, color=COLORS["BLUE"])
# manager.add_effect(RainbowChase, beats=16)
# manager.add_effect(FlashOnBeat, beats=4)
# manager.add_effect(WaveEffect, beats=8)
manager.add_effect(GameOfLife, beats=32)
print("Effects loaded! Cycling every few beats...")
print("Waiting for BPM signal...\n")

# =====================================================
# Run!
# =====================================================
try:
    manager.run(fps=30)
except KeyboardInterrupt:
    print("\nStopped!")
    pixels.fill(COLORS["OFF"])
    pixels.show()
