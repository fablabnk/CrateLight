import board
import neopixel

# Configure the pin connected to the NeoPixel data line
pixel_pin = board.GP28  # Change this to the GPIO pin you're using

# Total LEDs (excluding skipped ones)
num_leds = 300
leds_per_row = 24  # LEDs per row in your grid
num_rows = num_leds // leds_per_row  # Calculate the number of rows

# NeoPixel object
pixels = neopixel.NeoPixel(pixel_pin, num_leds, brightness=0.5, auto_write=False)
