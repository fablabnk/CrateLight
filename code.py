import board
import digitalio
import neopixel
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Configure the pin connected to the NeoPixel data line
pixel_pin = board.GP28  # Change this to the GPIO pin you're using

# Configure the number of pixels in your string
num_pixels = 50

# Create the NeoPixel object
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False)

# Define some colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

while True:
    # Fill the entire strip with red
    pixels.fill(RED)
    pixels.show()
    led.value = False
    time.sleep(1)

    # Color chase animations
    color_chase(GREEN, 0.05)
    color_chase(BLUE, 0.05)

    # Rainbow cycle animation
    rainbow_cycle(0.01)

    # Turn off all pixels
    pixels.fill(OFF)
    pixels.show()
    led.value = True
    time.sleep(1)
