The project is our version of the classic [C-Base 'Mate Light'](https://github.com/jaseg/matelight). The aim is to make a large scale pixel wall using bottle crates and LED strings, where each bottle represents a pixel and has one LED placed just inside the bottleneck. Our first implementation of this will be to build two 'crate towers' for our coding school's winter festival.

# About the LED Strings

We bought a set of WS2811 LED strings from AliExpress that run at 5V (not the 12V typically used in WS2811 LED strips). The strings use a three-wire system of power, data and ground, are chainable via connectors and also have bare-wire power injection points. The length of the wires between each LED is just slightly longer than the space between bottlenecks, making them ideal for this project. Also, in comparison to LED strips, they can easily bend around corners.

Each string has 50 LEDs, and each bottle crate contains 24 bottles/LEDs, so one string can drive just over 2 crates. Chaining is handled by the provided connectors, but as we need to bridge a larger gap between crates, it might be necessary to cut the strings in places (or perhaps more cleverly, skip an LED at this point).

For our initial 'crate towers', the plan is to provide power and data at the bottom and have each crate chain to the next from the top. This would keep all the tech 'down low' with short cable lengths. Data-wise, each crate would chain as follows ('I' for input, 'O' for output).

```
O - - - -
        |
  - - - -
  |
  - - - -
        |
I - - - -
```
# Power

It's best practice to use a dedicated power supply for the LED string(s). We shouldn't attempt to power it from any microcontroller we're using or use it to supply power to the microcontroller either. 

First off I wanted to estimated the total current draw for one string. In theory, each LED draws 55.5mA/0.055A at full white (RGB) brightness, so to power one full string we need 2.775 per (3A to be on the safe side).

For our first tests, I used a 65W USB charger, which was able to provide 3A through a type A connector. To provide power to the string, I butchered a type A to type B USB cable, removing the type B end and exposing the 4 wires and shielding. Here I kept the red and black wires, removed the shielding and cut back the other two coloured wires, placing heatshrink over them to prevent shorts. I then soldered the red and black wires to the exposed red/white and pure white 'power injection' cables on the LED strings.

I discovered that if I just power the LEDs and provide no data, none of them will light. This makes sense, but made it slightly tricker to tell at first if the string was being powered or not. To be sure, I measured the voltage across the outer power and ground pins of the connector with a multimeter.

# Data

To address the LEDs, I used a Raspberry Pi Pico running CircuitPython to provide voltage to the data line of the string from a GPIO output pin. I used the Mu editor to edit and flash a simple rainbow code example (see code.py in the repo). The code uses the neopixel library, which simplies things a lot and means we don't need to get into issues of timing etc.

I recommend using your PC to flash code and then to disconnect and power it separately (with a standard USB phone charger) before doing any probing/troubleshooting. I caused power surges on my laptop's USB port but luckily didn't blow it completely.

To send the data from the Pico, I used a breakout connector wire (which we bought along with the strings), which clips to the beginning of the LED string and exposes the power, data and ground wires. I soldered the data wire to GPIO pin 28 (physical pin 34 - not to be confused). I also soldered the ground wire to a Pico ground pin, meaning that the Pico and LED string power supplies share a common ground, which is also good pratice.

I had some issues getting the code to flash at first. I presumed that when code is saved to the Pico it is automatically flashed, which is typically true, but it's advisable to check the serial monitor pane for compilation or flashing errors, as this isn't visible by default. At first I didn't have the neopixel library installed and didn't notice for some time that my code wasn't being flashed. This causes a lot of headbashing working out why there wasn't any voltage on my GPIO pin. It helped to go back and flash a simple GPIO pin out code example first. One clue is that the onboard LED blinks twice intermittently using the default code supplied by the CircuitPython installation, but this flashing should stop when your own code is flashed. So if the blinking remains, your code didn't flash.

It is also worth noting that the Pico only outputs a maximum of 3.3V on it's GPIO pins. At first I thought I would need to implement a logic level shifter to ensure that the 3.3V is recognised as 'high' but according to Perplexity this is fine:

```
The WS2811 typically recognizes a 'high' signal when the voltage on the data line is approximately 2.5V or higher, while a 'low' signal is recognized when the voltage is around 0.8V or lower. This means that for reliable operation, the data signal should ideally be driven to at least 3.3V (which is common for many microcontroller outputs) to ensure it is interpreted as a 'high' signal.
```

# Next Steps

## Open Questions

Q: What is the maximum refresh rate and is it good enough for gaming?

Q: How often do we need to inject power?

A: The [Essager GaN chargers](https://www.aliexpress.com/item/1005004306745418.html) I bought for our lab's soldering irons can output 60W over the USB A connector, which is equivalent to 12A at 5V, which should be enough to power 4 strings (or 8 crates). This would mean we don't have to inject power to our towers at all, if operating them independently. But would we need thicker gauge wire than is used in a typical USB cable?

## Code Projects

### Volume Level Meters

### Tetris

### Expose control with an API?