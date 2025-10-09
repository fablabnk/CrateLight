"""Effect manager for cycling through multiple effects synced to BPM"""

import time


class EffectManager:
    """
    Manages multiple effects and cycles through them, optionally synced to BPM

    Usage:
        manager = EffectManager(pixels, width, height, hardware_config, clock)
        manager.add_effect(MyEffect1, beats=8)  # Run for 8 beats
        manager.add_effect(MyEffect2, beats=16) # Run for 16 beats
        manager.run(fps=30)
    """

    def __init__(self, pixels, width, height, hardware_config=None, clock=None):
        """
        Initialize effect manager

        Args:
            pixels: NeoPixel object
            width: Grid width
            height: Grid height
            hardware_config: Hardware configuration object
            clock: Clock source (BPMClock, FixedBPMClock, etc.)
        """
        self.pixels = pixels
        self.width = width
        self.height = height
        self.hardware_config = hardware_config
        self.clock = clock
        self.effects = []  # List of (EffectClass, kwargs) tuples
        self.current_effect_index = 0

    def add_effect(self, effect_class, beats=None, duration=None, **kwargs):
        """
        Add an effect to the rotation

        Args:
            effect_class: Effect class to instantiate
            beats: Number of beats to run (requires clock)
            duration: Duration in seconds (alternative to beats)
            **kwargs: Additional arguments to pass to effect __init__
        """
        self.effects.append({
            'class': effect_class,
            'beats': beats,
            'duration': duration,
            'kwargs': kwargs
        })

    def repeat_effect(self, effect_class, times=2, beats=None, duration=None, **kwargs):
        """
        Add the same effect multiple times

        Args:
            effect_class: Effect class to instantiate
            times: Number of times to repeat the effect
            beats: Number of beats to run each time (requires clock)
            duration: Duration in seconds each time (alternative to beats)
            **kwargs: Additional arguments to pass to effect __init__
        """
        for _ in range(times):
            self.add_effect(effect_class, beats=beats, duration=duration, **kwargs)

    def add_effect_sequence(self, effect_classes, beats=None, duration=None, **kwargs):
        """
        Add multiple effects with the same duration

        Args:
            effect_classes: List of effect classes to add
            beats: Number of beats to run each effect (requires clock)
            duration: Duration in seconds for each effect (alternative to beats)
            **kwargs: Additional arguments to pass to all effects
        """
        for effect_class in effect_classes:
            self.add_effect(effect_class, beats=beats, duration=duration, **kwargs)

    def run(self, fps=30):
        """Run the effect manager, cycling through effects"""
        if not self.effects:
            print("No effects added!")
            return

        frame_delay = 1.0 / fps

        while True:
            # Get current effect config
            effect_config = self.effects[self.current_effect_index]

            # Create effect instance with clock
            effect = effect_config['class'](
                self.pixels,
                self.width,
                self.height,
                self.hardware_config,
                clock=self.clock,
                **effect_config['kwargs']
            )

            # Determine how long to run
            beats = effect_config['beats']
            duration = effect_config['duration']

            if beats and self.clock:
                # Run for specified number of beats
                print(f"Running {effect.__class__.__name__} for {beats} beats")
                self._run_effect_beats(effect, beats, fps)
            elif duration:
                # Run for specified duration
                print(f"Running {effect.__class__.__name__} for {duration}s")
                self._run_effect_duration(effect, duration, fps)
            else:
                # Run until effect returns False
                print(f"Running {effect.__class__.__name__} until complete")
                self._run_effect_until_done(effect, fps)

            # Move to next effect
            self.current_effect_index = (self.current_effect_index + 1) % len(self.effects)

    def _run_effect_beats(self, effect, beats, fps):
        """Run effect for specified number of beats"""
        effect.setup()

        # Track beats
        beat_count = 0

        try:
            while beat_count < beats:
                # Update clock
                if self.clock:
                    self.clock.update()

                    # Check if beat occurred this frame
                    if self.clock.beat_occurred():
                        beat_count += 1
                        print(f"Beat {beat_count}/{beats}, BPM: {self.clock.get_bpm():.1f}")

                # Update effect
                should_continue = effect.update()
                self.pixels.show()
                effect.frame_count += 1

                if should_continue is False:
                    break

                time.sleep(1.0 / fps)
        finally:
            effect.cleanup()

    def _run_effect_duration(self, effect, duration, fps):
        """Run effect for specified duration in seconds"""
        effect.setup()
        start_time = time.monotonic()

        try:
            while time.monotonic() - start_time < duration:
                if self.clock:
                    self.clock.update()

                should_continue = effect.update()
                self.pixels.show()
                effect.frame_count += 1

                if should_continue is False:
                    break

                time.sleep(1.0 / fps)
        finally:
            effect.cleanup()

    def _run_effect_until_done(self, effect, fps):
        """Run effect until it returns False"""
        effect.setup()

        try:
            while True:
                if self.clock:
                    self.clock.update()

                should_continue = effect.update()
                self.pixels.show()
                effect.frame_count += 1

                if should_continue is False:
                    break

                time.sleep(1.0 / fps)
        finally:
            effect.cleanup()


class BPMSyncedEffect:
    """
    Mixin class for effects that sync to BPM clock

    Provides helpers for beat-synced animations
    """

    def get_beat_phase(self):
        """Get phase within current beat (0.0 to 1.0)"""
        if hasattr(self, 'clock') and self.clock:
            return self.clock.get_phase()
        return 0.0

    def get_bpm(self):
        """Get current BPM"""
        if hasattr(self, 'clock') and self.clock:
            return self.clock.get_bpm()
        return 60.0

    def is_beat(self, tolerance=0.1):
        """
        Check if we're on a beat

        Args:
            tolerance: How close to 0.0 phase to consider "on beat"
        """
        phase = self.get_beat_phase()
        return phase < tolerance
