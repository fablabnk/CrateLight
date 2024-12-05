# Combine Script

`combine.py` is a simple script that combines multiple Python files into a single file named `code.py`, stored in a `bin` directory. This is useful for deploying projects that require a single file, such as CircuitPython projects.

---

## Features
- Combines specified Python files into a single `code.py` file.
- Automatically sorts utility files by a dependency order for seamless integration.
- Ensures imports are consolidated at the top of the file.
- Automatically creates the `bin` folder if it does not exist.

---

## Dependency Management
The script respects a dependency order defined in the `combine.py` file. This ensures files like `imports.py` or `init.py` are combined in the correct order. You can customize the order by updating the `dependency_order` list:

```python
dependency_order = ["imports.py", "init.py", "colors.py", "grid_utils.py", "chase_fill.py"]
```

> **Tip:** Add all common imports to `imports.py` to keep your other files clean and modular.

---

## Usage

### 1. **Prepare Your Files**
- Place your Python files in a directory (default: `src/`).

### 2. **Update the File List**
- Open `combine.py` and review or update the `dependency_order` list.

### 3. **Run the Script**
- Execute the script:
  ```bash
  ./combine.py
  ```

### 4. **Output**
- The combined file will be saved as `bin/code.py`.

---

## Example
Given the following files in the `src/` folder:
- `imports.py`
- `init.py`
- `main.py`
- `colors.py`

Running the script will generate a combined `code.py` file in the `bin/` directory with:
1. Consolidated imports at the top.
2. Ordered utility file content.
3. `main.py` content appended at the end.

---

## Top Tips

- **Save on Transfer**:
  Press **Ctrl + Shift + S** in your editor to save over the `code.py` in the `bin` directory for easy transfer to your device.
  
- **Add Common Imports**:
  To keep your project modular, place shared imports in `imports.py`. This helps streamline your utility and main files.

