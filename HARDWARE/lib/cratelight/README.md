# CrateLight Library

A reusable LED animation library for Raspberry Pi Pico with NeoPixel LED grids.

## Installation

Copy the `lib/cratelight` folder to your project or add it to your Python path.

## Quick Start

```python
import sys
import board
import neopixel

sys.path.insert(0, '../lib')

from cratelight import COLORS, coords_to_id
from cratelight.effect_base import Effect

# Initialize hardware
pixel_pin = board.GP28
num_leds = 300
pixels = neopixel.NeoPixel(pixel_pin, num_leds, brightness=0.5, auto_write=False)

# Create a simple effect
class BlinkEffect(Effect):
    def setup(self):
        self.state = False

    def update(self):
        color = COLORS["RED"] if self.state else COLORS["OFF"]
        for i in range(len(self.pixels)):
            self.pixels[i] = color
        self.state = not self.state
        return True  # Run forever

# Run it
effect = BlinkEffect(pixels)
effect.run(fps=2)
```

## Creating Custom Effects

### Method 1: Using the Effect Base Class (Recommended)

The `Effect` base class provides a clean framework for creating effects:

```python
from cratelight.effect_base import Effect
from cratelight import COLORS, coords_to_id

class MyEffect(Effect):
    def setup(self):
        """Called once before starting - initialize variables here"""
        self.counter = 0
        self.color = COLORS["BLUE"]

    def update(self):
        """Called every frame - your animation logic goes here"""
        # Your animation code
        x = self.counter % self.width
        y = self.counter // self.width

        led_id = coords_to_id(x, y)
        if led_id is not None:
            self.pixels[led_id] = self.color

        self.counter += 1

        # Return False to stop, True to continue
        return self.counter < 100

    def cleanup(self):
        """Called once after finishing - optional"""
        # Clear the display
        for i in range(len(self.pixels)):
            self.pixels[i] = COLORS["OFF"]
```

### Method 2: Using Library Functions Directly

You can also use the library functions directly without the Effect class:

```python
from cratelight import clear_grid, color_coords, draw_from_grid, COLORS

# Clear the grid
clear_grid(pixels, 300)

# Color a specific coordinate
color_coords(pixels, 5, 3, COLORS["GREEN"])

# Draw a pattern
pattern = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
draw_from_grid(pixels, pattern, COLORS["BLUE"], COLORS["OFF"])
```

## Library Modules

### colors.py
- `COLORS`: Dictionary of predefined colors
- `get_random_color()`: Returns a random color

### grid_utils.py
- `coords_to_id(x, y)`: Convert grid coordinates to LED ID
- `id_to_coords(led_id)`: Convert LED ID to coordinates
- `clear_grid(pixels, num_leds)`: Turn off all LEDs
- `color_coords(pixels, x, y, color)`: Color a specific coordinate
- `color_id(pixels, id, color)`: Color a specific LED
- `draw_from_grid(pixels, drawing, color1, color2)`: Draw from 2D array

### animations.py
- `light_up_grid_horizontal(pixels, start, delay, color)`
- `light_up_grid_vertical(pixels, start, delay, color)`
- `light_up_grid(pixels, direction, start, delay, color)`

### game_of_life.py
- `gol_step(board)`: Execute one Game of Life generation

### pixel_map.py
- `create_pixel_representation(text)`: Convert text to pixel font

### effect_base.py
- `Effect`: Base class for creating custom effects

### clock.py
- `ClockSource`: Base class for timing sources
- `BPMClock`: Hardware BPM pulse detection
- `FixedBPMClock`: Fixed-rate BPM for testing
- `ManualClock`: Manually triggered beats

### utils.py
- `wheel(pos)`: Generate rainbow colors (0-255)
- `scale_color(color, brightness)`: Scale color by brightness
- `sine_wave(phase, power)`: Generate smooth wave from phase
- `lerp_color(color1, color2, t)`: Interpolate between colors

## Clock Synchronization

Effects can sync to external timing sources like BPM signals:

```python
from cratelight import BPMClock
from cratelight.effect_base import Effect

class SyncedEffect(Effect):
    def __init__(self, pixels, bpm_pin, width=24, height=12):
        super().__init__(pixels, width, height)
        self.clock = BPMClock(bpm_pin, default_bpm=120)

    def update(self):
        self.clock.update()  # Detect pulses
        phase = self.clock.get_phase()  # 0.0 to 1.0
        bpm = self.clock.get_bpm()

        # Use phase/bpm for timing your effect
        brightness = sine_wave(phase, power=2.0)
        # ... your effect code
```

Available clock types:
- **BPMClock**: Detects hardware pulses on a GPIO pin
- **FixedBPMClock**: Generates fixed-rate beats (for testing)
- **ManualClock**: Manually trigger beats via code

## Examples

Check the `examples/` folder for:
- `custom_effect_template.py`: Template for creating your own effects
- `example_game_of_life.py`: Conway's Game of Life implementation
- `example_rainbow_wave.py`: Rainbow wave effect
- `example_bpm_pulse.py`: BPM-synced pulse effect

## Contributing Effects

To contribute your own effect:

1. Copy `examples/custom_effect_template.py`
2. Rename it to describe your effect (e.g., `effect_fireworks.py`)
3. Implement your `setup()` and `update()` methods
4. Test it on your hardware
5. Submit a pull request!

## Grid Layout

The library assumes a 24x12 LED grid (288 LEDs) with a specific wiring pattern.
Coordinate (0, 0) is top-left, (23, 11) is bottom-right.

## Future Features

- [x] Clock synchronization support
- [ ] Effect sequencing/playlist
- [ ] Network/remote control
- [ ] More built-in effects
- [ ] Effect parameters/configuration system
- [ ] MIDI clock support
- [ ] Network time sync
