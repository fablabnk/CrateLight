

# Combine Script

`combine.py` is a simple yet powerful script that combines multiple Python files into a single file named `code2.py`, stored in a `bin` directory. This is particularly useful for deploying CircuitPython projects, which often require all code to be contained in a single `code.py` file.

---

## Features

- Combines all Python files from a source folder (`src/`) into a single `code2.py` file.
- **Dependency Order**: Automatically sorts utility files based on a predefined order for smooth integration.
- **Clean Imports**: Consolidates and deduplicates `import` and `from ... import ...` statements at the top of the file.
- Automatically creates the `bin` folder if it does not already exist.
- Modular: Allows you to develop code in separate files like a typical Python project.

---

## Dependency Management

The script respects a **dependency order** defined in the `combine.py` file. This ensures critical utility files are combined in the correct sequence.

You can customize the order by updating the `dependency_order` list:

```python
dependency_order = ["init.py", "colors.py", "grid_utils.py", "chase_fill.py"]
```

> **Tip:** Add shared imports or initialization logic to `init.py` for a clean and modular codebase.

---

## Usage

### 1. **Prepare Your Files**
- Place your Python files into a folder named `src` (default).
- Ensure you include a `main.py` file, as it serves as the entry point.

### 2. **Run the Script**
- Execute the script using Python:
  ```bash
  python3 combine.py
  ```
  or
  ```
  ./combine.py
  ```
  if you have python3 here /usr/bin/env python3

### 3. **Output**
- The combined output will be saved in the `bin` directory as `code2.py`.

---

## File Structure Example

Given the following files in the `src/` folder:

```
src/
│-- chase_fill.py
│-- colors.py
│-- fortytwo.py
│-- game_of_life.py
│-- grid_utils.py
│-- init.py
│-- main.py
│-- pixel_map.py
```

Running the script generates a `bin/code2.py` file that contains:

1. Consolidated imports at the top (deduplicated).
2. Content from utility files in the specified dependency order.
3. `main.py` content added at the end as the entry point.

---

## Explanation of Each Source File

Here’s a brief description of what each file is for:

### `init.py`
- Handles initialization logic for the project.
- Common functions, constants, or setup code go here.

### `colors.py`
- Defines color constants or functions for handling RGB/hex colors.
- Useful for managing color schemes for LED grids or animations.

### `grid_utils.py`
- Provides helper functions for creating and managing grids.
- Example: Generating a 2D grid structure or manipulating grid values.

### `chase_fill.py`
- Contains logic for animating a "chase fill" effect.
- Often used in LED matrices where lights "fill" in a specific pattern.

### `fortytwo.py`
- Prints 42 to screen

### `game_of_life.py`
- Implements Conway's Game of Life.
- Includes grid updates and logic for evolving the simulation.

### `pixel_map.py`
- Maps pixels or LEDs to specific coordinates.
- Often used for translating logical positions to physical displays.

### `main.py`
- The entry point for your project.
- Calls the functions and utilities from the above scripts to execute the program logic.

---

## Example Combined File (`code2.py`)

Here is what a sample combined file might look like:

```python
# Consolidated Imports
import time
from random import randint

# Utility Files Content
# init.py
def initialize():
    print("Initializing system...")

# colors.py
COLORS = ["RED", "GREEN", "BLUE"]

# grid_utils.py
def create_grid():
    return [[0] * 10 for _ in range(10)]

# chase_fill.py
def chase_fill(grid):
    print("Chasing and filling grid...")

# game_of_life.py
def update_game_of_life(grid):
    print("Updating Game of Life grid...")

# fortytwo.py
def get_forty_two():
    return 42

# pixel_map.py
def map_pixel(x, y):
    print(f"Mapping pixel at ({x}, {y})")

# Main Script Content
# main.py
initialize()
grid = create_grid()
chase_fill(grid)
update_game_of_life(grid)
print(f"Answer: {get_forty_two()}")
map_pixel(5, 5)
print("Done!")
```

---

## Top Tips

- **Save on Transfer**:
  Use your editor to save directly into the `bin/` directory for quick transfer to your microcontroller.

- **Modular Design**:
  Keep your project organized by splitting code into logical files. The script combines everything for deployment.

- **Custom Dependency Order**:
  Update the `dependency_order` list in `combine.py` to ensure files load correctly.

