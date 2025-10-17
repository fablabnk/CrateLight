"""
CrateLight - LED Effects Demo

This is your starting point! Customize this file to create your own LED show.
All you need to do is:
1. Configure your hardware setup below
2. Add/remove effects from the manager
3. Run on your Raspberry Pi Pico!
"""

import board
from cratelight import COLORS, BPMClock, FixedBPMClock, Font8x8, ZigzagGrid
from cratelight.effect_manager import EffectManager
from cratelight.effects.color_scroll import RainbowScroll
from cratelight.effects.flash import FlashOnBeat, StrobeEffect
from cratelight.effects.game_of_life import GameOfLife
from cratelight.effects.pulse import PulseOnBeat
from cratelight.effects.rainbow import RainbowChase
from cratelight.effects.random_fill import RandomStrobe
from cratelight.effects.scrolling import ScrollingText
from cratelight.effects.wave import WaveEffect
from cratelight.effects.rings import ConcentricRingsEffect
from cratelight.effects.knightrider import KnightRiderEffect
from cratelight.effects.sparkle import SparkleEffect


# =====================================================
# 🔧 HARDWARE CONFIGURATION
# =====================================================
# Pick the configuration that matches your LED setup!

# Example 1: Vertical zigzag grid (32x8 LEDs, columns alternate up/down)
config = ZigzagGrid(
    pin=board.GP2, width=32, height=8, brightness=0.1, direction="vertical"
)

# Example 2: Horizontal zigzag grid (rows alternate left/right)
# config = ZigzagGrid(pin=board.GP2, width=32, height=8, brightness=0.1, direction="horizontal")

# Example 3: CrateLight's custom 24x12 grid
# from cratelight import CrateLightGrid
# config = CrateLightGrid(pin=board.GP28, brightness=0.5)

# Example 4: Simple LED strip
# from cratelight import LEDStrip
# config = LEDStrip(pin=board.GP2, num_leds=256, brightness=0.1)

# Example 5: Linear grid (no zigzag, row-by-row)
# from cratelight import LinearGrid
# config = LinearGrid(pin=board.GP2, width=32, height=8, brightness=0.1)

# Create the pixel object
pixels = config.create_pixels()


# =====================================================
# ⏱️ BPM CLOCK CONFIGURATION
# =====================================================
# Choose how you want to time your effects!

# Option 1: Fixed BPM (good for testing and standalone use)
# clock = FixedBPMClock(bpm=140)

# Option 2: Hardware BPM detection (sync to music/external trigger)
# Uncomment these lines if you have a BPM signal on a GPIO pin:
clock = BPMClock(
    pin=board.GP15,           # Input pin for BPM signal
    default_bpm=120,          # Fallback BPM if no signal detected
    output_pin=board.GP16     # Optional: mirror signal to another pin
)

print(f"🎨 CrateLight Demo - {config.width}x{config.height} LEDs")
print(f"🎵 Using {clock.get_bpm()} BPM")
print("Press Ctrl+C to stop\n")


# =====================================================
# ✨ EFFECT MANAGER SETUP
# =====================================================
# The EffectManager cycles through your effects automatically!

manager = EffectManager(pixels, config.width, config.height, config, clock)

# Add your effects here! Each effect runs for a specified number of beats.
# Tip: Use beats=8/16/32 to sync with musical phrases
# All speeds now scale with BPM for tight sync!
# Use direction="random" for variety!

# Scrolling text with random direction
# manager.add_effect(
#     ScrollingText,
#     beats=16,
#     text="WELCOME TO THE FABLAB",
#     random_color=True,
#     speed=4,
#     font=Font8x8,
#     direction="random"
# )

# Rainbow chase with random direction (left/right/up/down)
# manager.add_effect(RainbowChase, beats=8, direction="random")

# # Rainbow scrolls with random directions - NOW USING CONSOLIDATED RainbowScroll!
# manager.add_effect(RainbowScroll, beats=16, axis="horizontal", speed=1.5, direction="random")
# manager.add_effect(RainbowScroll, beats=16, axis="vertical", speed=1.2, direction="random")

# # Strobe and flash effects
# manager.add_effect(StrobeEffect, beats=8, rainbow=True)
# manager.add_effect(FlashOnBeat, beats=8, rainbow=True)

# # Pulse effect
# manager.add_effect(PulseOnBeat, beats=12)
manager.add_effect(ConcentricRingsEffect, beats=16, origin="random", random_color=True)
manager.add_effect(KnightRiderEffect, beats=16, axis="horizontal", random_color=True)
manager.add_effect(SparkleEffect, beats=16, rainbow=True, density=12)
# # Game of Life with rainbow colors
# manager.add_effect(GameOfLife, beats=20, rainbow=True)

# # Wave effect
# manager.add_effect(WaveEffect, beats=12)

# # More variety
# manager.add_effect(RainbowChase, beats=8, direction="random")
# manager.add_effect(StrobeEffect, beats=8, random_color=True)
# manager.add_effect(RandomStrobe, duration=3, flashes=20)
# manager.add_effect(FlashOnBeat, beats=8, random_color=True)

print("✅ Effects loaded! Starting light show...")
print(f"📊 Total effects: {len(manager.effects)}\n")


# =====================================================
# 🚀 RUN THE SHOW!
# =====================================================
try:
    manager.run(fps=30)  # 30 frames per second
except KeyboardInterrupt:
    print("\n🛑 Stopped!")
    pixels.fill(COLORS["OFF"])
    pixels.show()
