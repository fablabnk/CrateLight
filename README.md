# CrateLight Library

A modular LED animation library for Raspberry Pi Pico with NeoPixel LED grids and strips.

## About

This project is our version of the classic [C-Base](https://www.c-base.org/) 'Mate Light'. The aim is to make a large scale pixel wall using bottle crates and LED strings, where each bottle represents a pixel and has one LED placed just inside the bottleneck. Our first implementation will be to build two 'crate towers' for our coding school's winter festival.

### Hardware

**LED Strings**
We use WS2811 LED strings running at 5V with a three-wire system (power, data, ground). Each string has 50 LEDs, and each bottle crate contains 24 bottles/LEDs, so one string can drive just over 2 crates. The strings are chainable via connectors and have bare-wire power injection points.

**Power**
Each LED draws approximately 55.5mA at full white brightness, requiring about 3A per string. We use dedicated power supplies (65W USB chargers providing 3A) to power the LED strings separately from the microcontroller.

**Data**
A Raspberry Pi Pico running CircuitPython provides voltage to the data line from a GPIO output pin. The Pico and LED string power supplies share a common ground. The Pico's 3.3V GPIO output is sufficient for the WS2811 data signal.

## Table of Contents

- [About](#about)
- [Using Pre-Built Effects](#using-pre-built-effects)
- [Creating Custom Effects](#creating-custom-effects)
- [Effect Manager](#effect-manager)
- [Available Effects](#available-effects)
- [Adding BPM Sync](#adding-bpm-sync)
- [Text Rendering](#text-rendering)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Features](#features)
- [Contributing](#contributing)

---

## Using Pre-Built Effects

```python
import sys
sys.path.insert(0, './lib')

from cratelight import EffectManager, LinearGrid, BPMClock
from cratelight.effects import PulseOnBeat, RainbowChase, StrobeEffect
import board

# Hardware setup
config = LinearGrid(pin=board.GP2, width=32, height=8, brightness=0.1)
pixels = config.create_pixels()
clock = BPMClock(pin=board.GP15, default_bpm=120)

# Create effect manager
manager = EffectManager(pixels, config.width, config.height, config, clock)

# Add effects - clean and simple
manager.add_effect(PulseOnBeat, beats=8)
manager.add_effect(RainbowChase, beats=16)
manager.repeat_effect(StrobeEffect, times=3, beats=4)

# Run
manager.run(fps=30)
```

---

## Creating Custom Effects

The `Effect` class provides a systematic way to create animations:

```python
from cratelight import Effect, COLORS

class StarfieldEffect(Effect):
    def setup(self):
        """Initialize once when effect starts"""
        self.stars = []
        # Initialize your effect state

    def update(self):
        """Run each frame - return True to continue, False to stop"""
        # Update star positions
        # Draw stars to self.pixels
        return True

    def cleanup(self):
        """Optional cleanup when effect ends"""
        pass
```

**Template available:** Copy `examples/custom_effect_template.py` to get started!

---

## Effect Manager

The EffectManager lets you sequence multiple effects:

```python
# Add single effect with duration
manager.add_effect(EffectClass, beats=8, duration=5.0)

# Repeat effect multiple times
manager.repeat_effect(EffectClass, times=3, beats=4)

# Add sequence with same duration
manager.add_effect_sequence([Effect1, Effect2, Effect3], beats=8)
```

---

## Available Effects

Pre-built effects in `cratelight.effects`:

- **PulseOnBeat** - Pulse brightness on each beat
- **WaveEffect** - Wave pattern synced to BPM
- **FlashOnBeat** - Sharp flash on each beat
- **StrobeEffect** - Multi-color strobe
- **RainbowChase** - Rainbow that moves with the beat
- **GameOfLife** - Conway's Game of Life cellular automaton
- **StaticText** - Display static text on LED grid
- **ScrollingText** - Scroll text across LED grid
- **BlinkingText** - Blinking text effect
- **CountdownEffect** - Countdown timer display

---

## Adding BPM Sync

```python
from cratelight import Effect, BPMClock, sine_wave, wheel, scale_color
import board

class BPMEffect(Effect):
    def __init__(self, pixels, width, height, hardware_config, bpm_pin):
        super().__init__(pixels, width, height, hardware_config)
        self.clock = BPMClock(bpm_pin, default_bpm=120)

    def setup(self):
        pass

    def update(self):
        self.clock.update()
        phase = self.clock.get_phase()

        # Pulse brightness synced to BPM
        brightness = sine_wave(phase, power=2.0)
        color = scale_color(wheel(self.frame_count % 256), brightness)

        # Fill all LEDs
        for i in range(len(self.pixels)):
            self.pixels[i] = color

        return True

# Use it
config = CrateLightGrid()
pixels = config.create_pixels()
effect = BPMEffect(pixels, config.width, config.height, config, board.GP15)
effect.run(fps=30)
```

**Clock options:**
- **BPMClock**: Hardware pulse detection
- **FixedBPMClock**: Fixed-rate testing
- **ManualClock**: Manual triggering

---

## Text Rendering

The library includes a built-in text rendering system for displaying text on LED grids:

```python
from cratelight import Font, TextRenderer, LinearGrid
from cratelight.effects import StaticText, ScrollingText, BlinkingText
import board

# Hardware setup
config = LinearGrid(pin=board.GP2, width=32, height=8, brightness=0.1)
pixels = config.create_pixels()

# Create text renderer
renderer = TextRenderer(pixels, config)

# Use with Effect Manager
from cratelight import EffectManager, BPMClock, COLORS

clock = BPMClock(pin=board.GP15, default_bpm=120)
manager = EffectManager(pixels, config.width, config.height, config, clock)

# Add text effects
manager.add_effect(StaticText, duration=3.0, text="HELLO", color=COLORS["RED"])
manager.add_effect(ScrollingText, duration=8.0, text="CRATELIGHT", color=COLORS["CYAN"])
manager.add_effect(BlinkingText, duration=4.0, text="ALERT", color=COLORS["ORANGE"])
manager.run(fps=30)

# Or use the renderer directly
renderer.center_text("HI", y_pos=1, fg_color=(255, 0, 0))
pixels.show()
```

**Text Effect Features:**
- 5x3 pixel font (26 letters, 10 numbers, 15 symbols)
- Hardware-agnostic rendering (works with any grid config)
- Static text display with centering or custom positioning
- Smooth scrolling text with configurable speed and direction
- Blinking text with adjustable blink rate
- Countdown timer effect
- Custom colors for foreground and background

---

## Architecture

### Design Philosophy

The library provides a reusable, extensible framework for LED animations with:

1. **Effect Base Class System** - Consistent interface for all animations
2. **Hardware Abstraction** - Same code works on strips, grids, different layouts
3. **Clock Synchronization** - Built-in BPM and timing support
4. **Modular Effects** - Each effect in its own file for easy discovery

### Usage Across Projects

The library can be used in any project:

```python
import sys
sys.path.insert(0, '/path/to/CrateLight/lib')

from cratelight import Effect, COLORS, BPMClock, Font, TextRenderer
from cratelight.effects import PulseOnBeat, RainbowChase, ScrollingText

# Use in your own projects!
```

---

## Project Structure

```
lib/cratelight/
├── effects/               Pre-built effects library
│   ├── pulse.py           Pulse and breathing effects
│   ├── wave.py            Wave patterns
│   ├── flash.py           Flash and strobe effects
│   ├── rainbow.py         Rainbow effects
│   ├── game_of_life.py    Conway's Game of Life
│   └── scrolling.py       Text effects (static, scrolling, blinking, countdown)
├── effect_base.py         Base Effect class
├── effect_manager.py      Effect sequencing and cycling
├── clock.py               BPM synchronization
├── hardware.py            Hardware configurations
├── text.py                Font and TextRenderer classes
├── colors.py              Color constants
├── utils.py               Color manipulation utilities
├── grid_utils.py          Grid coordinate mapping
└── README.md              Complete API reference

examples/                  Example implementations and templates
├── custom_effect_template.py
├── simple_text.py
└── text_demo.py
```

---

## Features

**Effect System**
- Modular effect architecture with base class
- Pre-built effects library (pulse, wave, flash, rainbow, strobe, text, Game of Life)
- Effect manager for sequencing and cycling
- BPM/clock synchronization support

**Hardware Support**
- Linear LED strips
- Zigzag grids
- Custom coordinate mappings
- Multiple hardware configurations

**Utilities**
- Text rendering with 5x3 pixel font (Font and TextRenderer classes)
- Grid coordinate mapping
- Color manipulation (scaling, interpolation, wheel)
- Wave generation and easing functions
- Game of Life implementation

**Developer Experience**
- Each effect in its own file for easy discovery
- Simple import system: `from cratelight.effects import EffectName`
- Clean code examples with minimal boilerplate
- Template for creating custom effects

---

## Contributing

### Creating a New Effect

1. Copy `examples/custom_effect_template.py`
2. Rename to describe your effect
3. Implement `setup()` and `update()` methods
4. Test and submit!

### Effect Guidelines

Effects should:
- Inherit from `Effect` base class
- Document what they do
- Include example usage
- Be self-contained (no hardcoded hardware beyond Effect constructor)
- Support both grid and strip modes where applicable

### Roadmap

1. **Effect Sequencer**: Queue multiple effects with transitions
2. **Network Control**: Control effects remotely
3. **MIDI Clock**: Sync to MIDI timing
4. **Effect Parameters**: Runtime configuration
5. **Web Interface**: Browser-based control

---

## Documentation

- `lib/cratelight/README.md` - Complete API reference
- `examples/custom_effect_template.py` - Template for new effects
- `examples/` - Working example implementations

---

## Usage in Your Project

1. Copy `lib/cratelight/` to your project
2. Import what you need:

```python
from cratelight import Effect, EffectManager, COLORS, BPMClock
from cratelight import Font, TextRenderer
from cratelight.effects import PulseOnBeat, RainbowChase, ScrollingText
```

No build scripts or file combining required. Pure Python, fully modular.
