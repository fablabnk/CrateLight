"""Clock and timing synchronization for LED effects"""

import time
import digitalio


class ClockSource:
    """Base class for timing/clock sources that effects can sync to"""

    def get_time(self):
        """Return current time in seconds"""
        return time.monotonic()

    def get_phase(self):
        """Return current phase (0.0 to 1.0) within the current beat/cycle"""
        return 0.0

    def get_bpm(self):
        """Return current BPM (beats per minute)"""
        return 60.0

    def update(self):
        """Called each frame to update timing state"""
        pass

    def beat_occurred(self):
        """Check if a beat occurred this frame (after calling update())"""
        return False


class BPMClock(ClockSource):
    """
    BPM-based clock that detects pulses from a hardware input pin.

    Example:
        clock = BPMClock(board.GP15, default_bpm=120)

        # In your effect update loop:
        clock.update()
        phase = clock.get_phase()  # 0.0 to 1.0
        bpm = clock.get_bpm()
    """

    def __init__(self, pin, default_bpm=60, pull=digitalio.Pull.DOWN, output_pin=None):
        """
        Initialize BPM clock

        Args:
            pin: GPIO pin for BPM input
            default_bpm: Default BPM before first pulse detected
            pull: Pull direction for input (Pull.DOWN or Pull.UP)
            output_pin: Optional GPIO pin to echo BPM pulses to
        """
        self.bpm_input = digitalio.DigitalInOut(pin)
        self.bpm_input.direction = digitalio.Direction.INPUT
        self.bpm_input.pull = pull

        # Optional output pin to echo BPM
        self.bpm_output = None
        if output_pin:
            self.bpm_output = digitalio.DigitalInOut(output_pin)
            self.bpm_output.direction = digitalio.Direction.OUTPUT
            self.bpm_output.value = False

        self.bpm = default_bpm
        self.last_pulse_time = None
        self.last_pin_state = False
        self.output_pulse_time = None
        self.output_pulse_duration = 0.05  # 50ms pulse
        self.pulse_this_frame = False  # Flag for beat detection

    def update(self):
        """Check for pulse and update BPM"""
        # Clear pulse flag at start of each frame
        self.pulse_this_frame = False

        current_state = self.bpm_input.value

        # Detect rising edge
        if current_state and not self.last_pin_state:
            self._on_pulse()

        self.last_pin_state = current_state

        # Handle output pulse timing
        if self.bpm_output and self.output_pulse_time:
            if time.monotonic() - self.output_pulse_time > self.output_pulse_duration:
                self.bpm_output.value = False
                self.output_pulse_time = None

    def _on_pulse(self):
        """Called when a pulse is detected"""
        now = time.monotonic()
        self.pulse_this_frame = True  # Set flag for this frame

        if self.last_pulse_time is not None:
            period = now - self.last_pulse_time
            if period > 0:
                # Calculate BPM from this pulse
                new_bpm = 60.0 / period
                # Smooth BPM with exponential moving average (alpha=0.3)
                # This reduces jitter while still adapting to tempo changes
                self.bpm = self.bpm * 0.7 + new_bpm * 0.3

        self.last_pulse_time = now

        # Echo pulse to output pin if configured
        if self.bpm_output:
            self.bpm_output.value = True
            self.output_pulse_time = now

    def get_bpm(self):
        """Get current BPM"""
        return self.bpm

    def get_phase(self):
        """
        Get current phase within beat (0.0 to 1.0)
        0.0 = start of beat, 1.0 = end of beat
        """
        if self.last_pulse_time is None:
            return 0.0

        time_since_pulse = time.monotonic() - self.last_pulse_time
        beat_period = 60.0 / self.bpm
        phase = (time_since_pulse / beat_period) % 1.0
        return phase

    def get_time_since_pulse(self):
        """Get time in seconds since last pulse"""
        if self.last_pulse_time is None:
            return 0.0
        return time.monotonic() - self.last_pulse_time

    def beat_occurred(self):
        """Check if a beat occurred this frame (after calling update())"""
        return self.pulse_this_frame


class FixedBPMClock(ClockSource):
    """
    Simple fixed-rate BPM clock for testing without hardware input

    Example:
        clock = FixedBPMClock(bpm=120)
        phase = clock.get_phase()
    """

    def __init__(self, bpm=60):
        """
        Initialize fixed BPM clock

        Args:
            bpm: Beats per minute (fixed)
        """
        self.bpm = bpm
        self.start_time = time.monotonic()

    def get_bpm(self):
        """Get current BPM"""
        return self.bpm

    def set_bpm(self, bpm):
        """Change the BPM"""
        self.bpm = bpm

    def get_phase(self):
        """Get current phase within beat (0.0 to 1.0)"""
        elapsed = time.monotonic() - self.start_time
        beat_period = 60.0 / self.bpm
        phase = (elapsed / beat_period) % 1.0
        return phase


class ManualClock(ClockSource):
    """
    Manually controlled clock for precise timing control

    Example:
        clock = ManualClock()
        clock.trigger_beat()  # Call this when beat should occur
        phase = clock.get_phase()
    """

    def __init__(self, default_bpm=60):
        """
        Initialize manual clock

        Args:
            default_bpm: Default BPM before first beat
        """
        self.bpm = default_bpm
        self.last_beat_time = None

    def trigger_beat(self):
        """Manually trigger a beat"""
        now = time.monotonic()
        if self.last_beat_time is not None:
            period = now - self.last_beat_time
            if period > 0:
                self.bpm = 60.0 / period
        self.last_beat_time = now

    def get_bpm(self):
        """Get current BPM"""
        return self.bpm

    def get_phase(self):
        """Get current phase within beat (0.0 to 1.0)"""
        if self.last_beat_time is None:
            return 0.0

        time_since_beat = time.monotonic() - self.last_beat_time
        beat_period = 60.0 / self.bpm
        phase = (time_since_beat / beat_period) % 1.0
        return phase
