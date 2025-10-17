# Contributing to CrateLight

Thank you for your interest in contributing to CrateLight! We welcome contributions from the community.

## How to Contribute

### Creating a New Effect

The easiest way to contribute is by creating a new LED effect:

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/CrateLight.git
   cd CrateLight
   ```

3. **Create a new branch** for your effect:
   ```bash
   git checkout -b effect/your-effect-name
   ```

4. **Create your effect file** in `lib/cratelight/effects/`:
   ```python
   """Your effect description"""

   from ..effect_base import Effect
   from ..effect_manager import BPMSyncedEffect
   from ..colors import COLORS

   class YourEffect(Effect, BPMSyncedEffect):
       """
       Brief description of what your effect does

       Usage:
           manager.add_effect(YourEffect, beats=8, param=value)
       """

       def __init__(self, pixels, width=24, height=12, hardware_config=None, clock=None):
           super().__init__(pixels, width, height, hardware_config, clock)
           # Your init code

       def setup(self):
           """Initialize your effect"""
           pass

       def update(self):
           """Run each frame - return True to continue, False to stop"""
           # Your animation code
           return True

       def cleanup(self):
           """Optional cleanup when effect ends"""
           self.pixels.fill(COLORS["OFF"])
   ```

5. **Add your effect to the exports** in `lib/cratelight/effects/__init__.py`:
   ```python
   from .your_effect import YourEffect

   __all__ = [
       # ... existing effects ...
       'YourEffect',
   ]
   ```

6. **Test your effect** (see Testing section below)

7. **Commit your changes**:
   ```bash
   git add lib/cratelight/effects/your_effect.py
   git add lib/cratelight/effects/__init__.py
   git commit -m "Add YourEffect: brief description"
   ```

8. **Push to your fork**:
   ```bash
   git push origin effect/your-effect-name
   ```

9. **Open a Pull Request** on GitHub:
   - Go to the original CrateLight repository
   - Click "Pull Requests" → "New Pull Request"
   - Click "compare across forks"
   - Select your fork and branch
   - Fill in the PR template with:
     - What your effect does
     - Any special parameters it accepts
     - Example usage
     - (Optional) Video/GIF of the effect in action

## Testing Your Contribution

### Hardware Testing
TODO: Add hardware testing guidelines once test setup is standardized

For now, test your effect on any CircuitPython-compatible board with NeoPixels:
- Raspberry Pi Pico
- ESP32-S2/S3
- Any board running CircuitPython 7.0+

### Software Testing
TODO: Add unit tests and simulation testing framework

Currently: Manually verify your effect works with different hardware configs:
```python
from cratelight import ZigzagGrid, LEDStrip
from cratelight.effects import YourEffect

# Test on different hardware
configs = [
    ZigzagGrid(pin=board.GP2, width=32, height=8),
    LEDStrip(pin=board.GP2, num_leds=256),
]
```

## Code Style Guidelines

- **Follow PEP 8** for Python code style
- **Use descriptive variable names**: `brightness`, `color_offset`, not `b`, `co`
- **Add docstrings** to all classes and public methods
- **Use constants** for magic numbers:
  ```python
  # Good
  FADE_RATE = 0.15
  brightness *= (1.0 - FADE_RATE)

  # Avoid
  brightness *= 0.85
  ```
- **Import order**: Standard library → Third party → Local imports
- **Keep effects self-contained**: Don't modify other effects or core modules

## Effect Design Guidelines

Good effects should:
- ✅ Support both grid and strip configurations
- ✅ Work with or without BPM clock
- ✅ Be configurable via `__init__` parameters
- ✅ Clean up in `cleanup()` method (turn off LEDs)
- ✅ Document parameters in docstring with usage example
- ✅ Use descriptive class names (e.g., `SparkleEffect`, not `Effect7`)

## Pull Request Process

1. **One effect per PR**: Keep PRs focused on a single new effect
2. **Descriptive title**: "Add SparkleEffect" not "New effect"
3. **Fill out PR description**:
   - What the effect does
   - Parameters it accepts
   - Example code showing how to use it
4. **Be responsive**: Address review feedback promptly
5. **Squash commits** if requested before merge

## Questions or Issues?

- **Bug reports**: Open an issue with steps to reproduce
- **Feature requests**: Open an issue describing what you'd like to see
- **Questions**: Open a discussion or issue

## Future Contribution Areas

The following areas need work (contributions welcome!):

- 🔨 **Testing Framework**: Unit tests and hardware simulation
- 📚 **Examples Directory**: Example projects using the library
- 🎨 **More Effects**: We always want more creative effects!
- 📖 **Documentation**: API docs, tutorials, guides
- 🔧 **Tools**: Effect simulator, hardware mapper generator

## License

By contributing to CrateLight, you agree that your contributions will be licensed under the Apache 2.0 License.
