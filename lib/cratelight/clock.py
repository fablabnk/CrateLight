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
        self.default_bpm = default_bpm
        self.last_pulse_time = None
        self.last_pin_state = False
        self.output_pulse_time = None
        self.output_pulse_duration = 0.05  # 50ms pulse
        self.pulse_this_frame = False  # Flag for beat detection

        # Advanced BPM tracking with moving median filter
        self.pulse_history = []  # Store last N pulse intervals
        self.history_size = 8  # Use last 8 intervals for median
        self.timeout_seconds = 3.0  # Reset if no pulse for 3 seconds

    def update(self):
        """Check for pulse and update BPM"""
        # Clear pulse flag at start of each frame
        self.pulse_this_frame = False

        current_state = self.bpm_input.value

        # Detect rising edge
        if current_state and not self.last_pin_state:
            self._on_pulse()

        self.last_pin_state = current_state

        # Check for timeout - reset to default if no pulse for too long
        if self.last_pulse_time is not None:
            time_since_pulse = time.monotonic() - self.last_pulse_time
            if time_since_pulse > self.timeout_seconds:
                # Reset to default BPM and clear history
                self.bpm = self.default_bpm
                self.pulse_history = []
                self.last_pulse_time = None

        # Handle output pulse timing
        if self.bpm_output and self.output_pulse_time:
            if time.monotonic() - self.output_pulse_time > self.output_pulse_duration:
                self.bpm_output.value = False
                self.output_pulse_time = None

    def _median(self, values):
        """Calculate median of a list (simple implementation for CircuitPython)"""
        if not values:
            return 0.0
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        if n % 2 == 0:
            return (sorted_vals[n//2 - 1] + sorted_vals[n//2]) / 2.0
        return sorted_vals[n//2]

    def _on_pulse(self):
        """Called when a pulse is detected"""
        now = time.monotonic()
        self.pulse_this_frame = True  # Set flag for this frame

        if self.last_pulse_time is not None:
            period = now - self.last_pulse_time

            # Sanity check: reject obviously wrong intervals
            # BPM range: 40-240 (period range: 1.5s to 0.25s)
            if 0.25 <= period <= 1.5:
                # Add to history
                self.pulse_history.append(period)

                # Keep only last N intervals
                if len(self.pulse_history) > self.history_size:
                    self.pulse_history.pop(0)

                # Calculate BPM using median of recent intervals
                # Median is much better than average at rejecting outliers!
                if len(self.pulse_history) >= 3:
                    # Use median for stability
                    median_period = self._median(self.pulse_history)
                    new_bpm = 60.0 / median_period

                    # Light smoothing with EMA (alpha=0.5 for faster response)
                    self.bpm = self.bpm * 0.5 + new_bpm * 0.5
                else:
                    # Not enough history yet, use simple calculation
                    self.bpm = 60.0 / period
            else:
                # Bad pulse - don't update last_pulse_time to avoid phase drift
                print(f"BPM: Rejected bad pulse interval: {period:.3f}s")
                self.pulse_this_frame = False
                return

        # CRITICAL: Update last_pulse_time AFTER validation
        # This ensures phase calculation stays locked to valid beats
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

        IMPORTANT: Phase is locked to actual pulse timing, not smoothed BPM.
        This prevents drift and keeps animations tight to the beat!
        """
        if self.last_pulse_time is None:
            return 0.0

        time_since_pulse = time.monotonic() - self.last_pulse_time

        # Use the median period directly for phase calculation
        # This locks phase to actual pulse intervals, not smoothed BPM
        if len(self.pulse_history) >= 3:
            beat_period = self._median(self.pulse_history)
        else:
            # Fall back to BPM-based calculation if not enough history
            beat_period = 60.0 / self.bpm

        # Calculate phase, clamped to [0.0, 1.0]
        # We clamp rather than wrap because we want to "stick" at 1.0
        # until the next beat arrives, which resets last_pulse_time
        phase = time_since_pulse / beat_period

        # If we're past 1.0, it means we're waiting for the next beat
        # Stay at 0.95 to avoid visual "jumping" back to 0
        if phase > 1.0:
            phase = 0.95

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
        clock.update()  # Call this each frame
        if clock.beat_occurred():
            print("Beat!")
    """

    def __init__(self, bpm=60):
        """
        Initialize fixed BPM clock

        Args:
            bpm: Beats per minute (fixed)
        """
        self.bpm = bpm
        self.start_time = time.monotonic()
        self.last_beat_number = -1
        self.beat_this_frame = False

    def update(self):
        """Called each frame to update beat detection"""
        self.beat_this_frame = False

        # Calculate which beat number we're currently in
        elapsed = time.monotonic() - self.start_time
        beat_period = 60.0 / self.bpm
        current_beat_number = int(elapsed / beat_period)

        # Check if we've crossed into a new beat
        if current_beat_number > self.last_beat_number:
            self.beat_this_frame = True
            self.last_beat_number = current_beat_number

    def beat_occurred(self):
        """Check if a beat occurred this frame (after calling update())"""
        return self.beat_this_frame

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
