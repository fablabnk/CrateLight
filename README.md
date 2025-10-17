# CrateLight Library

A modular LED animation library for Raspberry Pi Pico with NeoPixel LED grids and strips.

## Table of Contents

- [Quick Start](#quick-start)
  - [Hardware Setup](#hardware-setup)
  - [Simple Effect Example](#simple-effect-example)
  - [Complete Working Example](#complete-working-example)
- [Using Pre-Built Effects](#using-pre-built-effects)
- [Creating Custom Effects](#creating-custom-effects)
- [Effect Manager](#effect-manager)
- [Available Effects](#available-effects)
- [Adding BPM Sync](#adding-bpm-sync)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Features](#features)
- [Contributing](#contributing)

---

## Quick Start

### Hardware Setup

Choose your hardware configuration:

```python
import sys
sys.path.insert(0, './lib')

from cratelight import CrateLightGrid, LEDStrip, ZigzagGrid, LinearGrid
import board

# Option A: CrateLight 24x12 Grid
config = CrateLightGrid(pin=board.GP28, brightness=0.5)

# Option B: LED Strip (256 LEDs)
# config = LEDStrip(pin=board.GP2, num_leds=256, brightness=0.1)

# Option C: Zigzag Grid (32x8)
# config = ZigzagGrid(pin=board.GP2, width=32, height=8, brightness=0.1)

# Option D: Linear Grid (32x8)
# config = LinearGrid(pin=board.GP2, width=32, height=8, brightness=0.1)

# Create the pixels object
pixels = config.create_pixels()
```

### Simple Effect Example

```python
from cratelight import Effect, COLORS

class MyEffect(Effect):
    def setup(self):
        """Initialize your effect"""
        self.counter = 0

    def update(self):
        """Run each frame"""
        # Example: Light up LEDs one by one
        y = self.counter // self.width
        x = self.counter % self.width

        led_id = self.coords_to_id(x, y)
        if led_id is not None:
            self.pixels[led_id] = COLORS["RED"]

        self.counter += 1
        return self.counter < (self.width * self.height)

# Create and run effect
effect = MyEffect(pixels, config.width, config.height, config)
effect.run(fps=30)
```

### Complete Working Example

```python
import sys
sys.path.insert(0, './lib')

import board
from cratelight import Effect, COLORS, CrateLightGrid

# 1. Configure hardware
config = CrateLightGrid(pin=board.GP28, brightness=0.5)
pixels = config.create_pixels()

# 2. Create effect
class BlinkEffect(Effect):
    def setup(self):
        self.state = False

    def update(self):
        color = COLORS["BLUE"] if self.state else COLORS["OFF"]
        for i in range(len(self.pixels)):
            self.pixels[i] = color
        self.state = not self.state
        return True

# 3. Run it
effect = BlinkEffect(pixels, config.width, config.height, config)
effect.run(fps=2)
```

**The beauty:** Same effect code works on different hardware! Just swap the config line.

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

## Architecture

### Design Philosophy

The library provides a reusable, extensible framework for LED animations with:

1. **Effect Base Class System** - Consistent interface for all animations
2. **Hardware Abstraction** - Same code works on strips, grids, different layouts
3. **Clock Synchronization** - Built-in BPM and timing support
4. **Modular Effects** - Each effect in its own file for easy discovery

### Before vs After

**Before (Modular_circuit_code):**
- ❌ Code scattered across multiple files
- ❌ `combine.py` script needed to merge files
- ❌ Hard to reuse in other projects
- ❌ No systematic effect creation
- ❌ No clock synchronization

**After (lib/cratelight):**
- ✅ Clean library structure
- ✅ Import and use in any project
- ✅ Effect base class for consistency
- ✅ Clock synchronization built-in
- ✅ Easy for contributors to add effects
- ✅ Reusable utilities
- ✅ Examples and templates provided

### Usage Across Projects

The library can be used in any project:

```python
import sys
sys.path.insert(0, '/path/to/CrateLight/lib')

from cratelight import Effect, COLORS, BPMClock
from cratelight.effects import PulseOnBeat, RainbowChase

# Use in your own projects!
```

---

## Project Structure

```
lib/cratelight/
├── effects/            Pre-built effects library
│   ├── pulse.py        Pulse and breathing effects
│   ├── wave.py         Wave patterns
│   ├── flash.py        Flash and strobe effects
│   └── rainbow.py      Rainbow effects
├── effect_base.py      Base Effect class
├── effect_manager.py   Effect sequencing and cycling
├── clock.py            BPM synchronization
├── hardware.py         Hardware configurations
├── colors.py           Color constants
├── utils.py            Color manipulation utilities
├── grid_utils.py       Grid coordinate mapping
├── game_of_life.py     Conway's Game of Life
└── README.md           Complete API reference

examples/               Example implementations and templates
```

---

## Features

**Effect System**
- Modular effect architecture with base class
- Pre-built effects library (pulse, wave, flash, rainbow, strobe)
- Effect manager for sequencing and cycling
- BPM/clock synchronization support

**Hardware Support**
- Linear LED strips
- Zigzag grids
- Custom coordinate mappings
- Multiple hardware configurations

**Utilities**
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

We welcome contributions from the community! See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Start for Contributors

1. Fork the repository
2. Create a new branch for your effect
3. Add your effect to `lib/cratelight/effects/`
4. Test with different hardware configurations
5. Submit a pull request

### Creating a New Effect

1. Copy `examples/custom_effect_template.py`
2. Rename to describe your effect
3. Implement `setup()` and `update()` methods
4. Add to `lib/cratelight/effects/__init__.py`
5. Test and submit a PR!

### Effect Guidelines

Effects should:
- Inherit from `Effect` base class
- Document what they do
- Include example usage
- Be self-contained (no hardcoded hardware beyond Effect constructor)
- Support both grid and strip modes where applicable

See [CONTRIBUTING.md](CONTRIBUTING.md) for complete guidelines and code style requirements.

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
from cratelight.effects import PulseOnBeat, RainbowChase
```

No build scripts or file combining required. Pure Python, fully modular.
