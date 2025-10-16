"""
GFX Font Text Demo - Better looking text with Adafruit bitmap fonts

This example shows how to use larger, more readable fonts with your LED grid.

Installation:
    1. Install adafruit_bitmap_font library:
       circup install adafruit_bitmap_font

    2. Download fonts from:
       https://github.com/adafruit/Adafruit_CircuitPython_Bitmap_Font/tree/main/examples/fonts

    3. Copy .bdf or .pcf font files to your Pico in a /fonts/ directory

Font recommendations by grid size:
    - 8x8 grid: Use 5x7 or 6x10 fonts
    - 16x8 grid: Use 8x13 or 10x16 fonts
    - 24x12 grid: Use 10x16 or 12x24 fonts
    - 32x8 grid: Use 8x13, 10x16, or 12x24 fonts
"""

import board
from cratelight import COLORS, FixedBPMClock, ZigzagGrid, HAS_GFX_FONTS
from cratelight.effect_manager import EffectManager

# Check if GFX fonts are available
if not HAS_GFX_FONTS:
    print("WARNING: GFX fonts not available!")
    print("Install: circup install adafruit_bitmap_font")
    print("Falling back to simple built-in fonts...\n")

# =====================================================
# Hardware Configuration
# =====================================================
config = ZigzagGrid(pin=board.GP2, width=32, height=8, brightness=0.1, direction="vertical")
pixels = config.create_pixels()
clock = FixedBPMClock(bpm=120)

print(f"GFX Text Demo - {config.width}x{config.height} LEDs")
print(f"HAS_GFX_FONTS: {HAS_GFX_FONTS}\n")

# =====================================================
# Load Font (optional)
# =====================================================
font = None

if HAS_GFX_FONTS:
    try:
        from adafruit_bitmap_font import bitmap_font

        # Try to load a font file
        # Adjust path and filename to match your setup
        font_paths = [
            "/fonts/Arial-12.bdf",
            "/fonts/helvR10.bdf",
            "/fonts/6x10.bdf",
        ]

        for font_path in font_paths:
            try:
                font = bitmap_font.load_font(font_path)
                print(f"✓ Loaded font: {font_path}")
                break
            except (OSError, ValueError):
                continue

        if font is None:
            print("✗ No font files found")
            print(f"  Tried: {font_paths}")
            print("  Using simple built-in font instead\n")
    except ImportError:
        print("✗ adafruit_bitmap_font not installed")
        print("  Install with: circup install adafruit_bitmap_font")
        print("  Using simple built-in font instead\n")

# =====================================================
# Setup Effects
# =====================================================
manager = EffectManager(pixels, config.width, config.height, config, clock)

# Import GFX effects
from cratelight.effects.scrolling_gfx import GFXScrollingText, GFXStaticText

# Add GFX text effects
if font:
    # With custom font
    manager.add_effect(
        GFXScrollingText,
        beats=16,
        text="CUSTOM FONT!",
        font=font,
        color=COLORS["CYAN"],
        random_color=False
    )
else:
    # With built-in simple font (8x8)
    manager.add_effect(
        GFXScrollingText,
        beats=16,
        text="BUILT-IN",
        font=None,  # Uses SimpleGFXTextRenderer
        color=COLORS["GREEN"],
        random_color=False
    )

# Add a static text display
manager.add_effect(
    GFXStaticText,
    duration=3,
    text="STOP",
    font=font,
    color=COLORS["RED"],
    centered=True
)

# Add more scrolling text with different options
manager.add_effect(
    GFXScrollingText,
    beats=16,
    text="RAINBOW MODE",
    font=font,
    random_color=True,
    speed=2
)

print("✅ Effects loaded!")
print(f"📊 Total effects: {len(manager.effect_queue)}\n")

# =====================================================
# Run!
# =====================================================
try:
    manager.run(fps=30)
except KeyboardInterrupt:
    print("\n🛑 Stopped!")
    pixels.fill(COLORS["OFF"])
    pixels.show()


# =====================================================
# Notes on Getting Fonts
# =====================================================
"""
Where to get bitmap fonts:

1. Adafruit's collection:
   https://github.com/adafruit/Adafruit_CircuitPython_Bitmap_Font/tree/main/examples/fonts

2. Convert your own TTF fonts to BDF:
   Use online converters or FontForge

3. Popular fonts for LED displays:
   - tom-thumb.bdf (3x5, super tiny)
   - 6x10.bdf (good for 32x8 grids)
   - helvR10.bdf (Helvetica 10pt)
   - courR10.bdf (Courier 10pt)

4. Copy fonts to your Pico:
   - Create a /fonts/ folder on CIRCUITPY drive
   - Copy .bdf or .pcf files there
   - Reference them by path in your code
"""
